import asyncio
import json
import os
from typing import List, Dict, Any, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

# Check if using mock or real Hindsight
USE_MOCK_HINDSIGHT = os.getenv("USE_MOCK_HINDSIGHT", "true").lower() == "true"


class HindsightMemory:
    def __init__(
        self,
        id: str,
        text: str,
        metadata: Dict[str, Any],
        score: float = 0.0,
    ):
        self.id = id
        self.text = text
        self.metadata = metadata
        self.score = score


class HindsightClient:
    """Adapter for the official Hindsight Cloud SDK."""

    def __init__(self):
        from src.config import settings
        from hindsight_client import Hindsight

        self.base_url = settings.HINDSIGHT_BASE_URL.rstrip("/")
        self._client = Hindsight(
            base_url=self.base_url,
            api_key=settings.HINDSIGHT_API_KEY,
            timeout=30.0,
        )

    async def close(self):
        await self._client.aclose()

    @staticmethod
    def _metadata_to_sdk(metadata: Dict[str, Any]) -> Dict[str, str]:
        return {key: json.dumps(value, default=str) for key, value in metadata.items()}

    @staticmethod
    def _metadata_from_sdk(metadata: Optional[Dict[str, str]]) -> Dict[str, Any]:
        decoded = {}
        for key, value in (metadata or {}).items():
            try:
                decoded[key] = json.loads(value)
            except (TypeError, json.JSONDecodeError):
                decoded[key] = value
        return decoded

    @classmethod
    def _memory_from_response(cls, result: Any) -> HindsightMemory:
        scores = getattr(result, "scores", None)
        score = getattr(scores, "final", 0.0) if scores else 0.0
        return HindsightMemory(
            id=result.id,
            text=result.text,
            metadata=cls._metadata_from_sdk(getattr(result, "metadata", None)),
            score=float(score or 0.0),
        )

    async def recall(
        self,
        bank_id: str,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        min_score: float = 0.0,
    ) -> List[HindsightMemory]:
        try:
            resp = await self._client.arecall(bank_id=bank_id, query=query)
            results = getattr(resp, "results", []) or []
            memories = [self._memory_from_response(m) for m in results]
            if min_score > 0:
                memories = [m for m in memories if m.score >= min_score]
            return memories[:top_k]
        except Exception as e:
            logger.error(f"Hindsight recall error: {e}")
            return []

    async def retain(
        self,
        bank_id: str,
        text: str,
        metadata: Dict[str, Any],
        merge_policy: Optional[Dict[str, Any]] = None,
    ) -> HindsightMemory:
        try:
            resp = await self._client.aretain(
                bank_id=bank_id,
                content=text,
                metadata=self._metadata_to_sdk(metadata),
            )
            op_id = getattr(resp, "operation_id", None) or str(uuid.uuid4())[:8]
            return HindsightMemory(
                id=op_id,
                text=text,
                metadata=metadata,
                score=1.0,
            )
        except Exception as e:
            logger.warning(f"Hindsight retain initial attempt failed, ensuring bank exists: {e}")
            try:
                await self._create_bank(bank_id)
                resp = await self._client.aretain(
                    bank_id=bank_id,
                    content=text,
                    metadata=self._metadata_to_sdk(metadata),
                )
                op_id = getattr(resp, "operation_id", None) or str(uuid.uuid4())[:8]
                return HindsightMemory(
                    id=op_id,
                    text=text,
                    metadata=metadata,
                    score=1.0,
                )
            except Exception as err:
                logger.error(f"Hindsight retain retry failed: {err}")
                raise

    async def _create_bank(self, bank_id: str):
        try:
            await self._client.acreate_bank(bank_id=bank_id)
            logger.info(f"Created bank: {bank_id}")
        except Exception as e:
            logger.warning(f"Create bank note: {bank_id}: {e}")

    async def recall_both(
        self,
        deal_id: str,
        rep_id: str,
        query: str,
        top_k: int = 10,
    ) -> List[HindsightMemory]:
        from src.config import get_project_bank, get_common_bank
        project_bank = get_project_bank(deal_id)
        common_bank = get_common_bank(rep_id)

        project_results, common_results = await asyncio.gather(
            self.recall(project_bank, query, top_k),
            self.recall(common_bank, query, top_k),
        )

        all_results = list(project_results) + list(common_results)
        all_results.sort(key=lambda m: (-m.score, -m.metadata.get("frequency", 1)))
        return all_results[:top_k]


class MockHindsightClient:
    """In-memory mock of Hindsight for demo"""
    
    def __init__(self):
        self.banks: Dict[str, List[HindsightMemory]] = {}
    
    def _get_bank(self, bank_id: str) -> List[HindsightMemory]:
        if bank_id not in self.banks:
            self.banks[bank_id] = []
        return self.banks[bank_id]
    
    def _memory_from_data(self, data: Dict) -> HindsightMemory:
        return HindsightMemory(
            id=data.get("id", str(uuid.uuid4())),
            text=data.get("text", ""),
            metadata=data.get("metadata", {}),
            score=data.get("score", 0.0),
        )

    async def recall(
        self,
        bank_id: str,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        min_score: float = 0.0,
    ) -> List[HindsightMemory]:
        bank = self._get_bank(bank_id)
        
        query_lower = query.lower()
        results = []
        
        for mem in bank:
            mem_text_lower = mem.text.lower()
            score = 0.0
            for term in query_lower.split():
                if term in mem_text_lower:
                    score += 1.0
            
            freq = mem.metadata.get("frequency", 1)
            score += freq * 0.1
            
            if score > 0:
                results.append((mem, score))
        
        results.sort(key=lambda x: -x[1])
        return [self._memory_from_data({
            "id": m.id,
            "text": m.text,
            "metadata": m.metadata,
            "score": s,
        }) for m, s in results[:top_k]]

    async def retain(
        self,
        bank_id: str,
        text: str,
        metadata: Dict[str, Any],
        merge_policy: Optional[Dict[str, Any]] = None,
    ) -> HindsightMemory:
        bank = self._get_bank(bank_id)
        
        if merge_policy and merge_policy.get("target_id"):
            target_id = merge_policy["target_id"]
            for mem in bank:
                if mem.id == target_id:
                    if "text" in merge_policy:
                        mem.text = merge_policy["text"]
                    mem.metadata["frequency"] = merge_policy.get("new_frequency", mem.metadata.get("frequency", 1) + 1)
                    mem.metadata["evidence_count"] = merge_policy.get("new_evidence_count", mem.metadata.get("evidence_count", 1) + 1)
                    mem.metadata["last_seen"] = merge_policy.get("new_last_seen", "")
                    if "provenance" in merge_policy:
                        existing_prov = mem.metadata.get("provenance", {})
                        new_prov = merge_policy["provenance"]
                        existing_quotes = existing_prov.get("source_quotes", [])
                        new_quotes = new_prov.get("source_quotes", [])
                        existing_prov["source_quotes"] = existing_quotes + new_quotes
                        mem.metadata["provenance"] = existing_prov
                    return mem
        
        mem_id = str(uuid.uuid4())[:8]
        mem = HindsightMemory(
            id=mem_id,
            text=text,
            metadata=metadata,
            score=1.0,
        )
        bank.append(mem)
        logger.info(f"Mock Hindsight: Stored memory in {bank_id}: {text[:50]}...")
        return mem

    async def recall_both(
        self,
        deal_id: str,
        rep_id: str,
        query: str,
        top_k: int = 10,
    ) -> List[HindsightMemory]:
        from src.config import get_project_bank, get_common_bank
        project_bank = get_project_bank(deal_id)
        common_bank = get_common_bank(rep_id)

        project_results = await self.recall(project_bank, query, top_k)
        common_results = await self.recall(common_bank, query, top_k)

        all_results = list(project_results) + list(common_results)
        all_results.sort(key=lambda m: (-m.score, -m.metadata.get("frequency", 1)))
        return all_results[:top_k]


# Select client based on environment variable
if USE_MOCK_HINDSIGHT:
    hindsight_client = MockHindsightClient()
    logger.info("Using Mock Hindsight Client")
else:
    hindsight_client = HindsightClient()
    logger.info("Using Real Hindsight Cloud Client")