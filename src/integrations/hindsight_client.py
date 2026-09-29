import httpx
import asyncio
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
    """Real Hindsight Cloud API client"""
    
    def __init__(self):
        from src.config import settings
        self.base_url = settings.HINDSIGHT_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.HINDSIGHT_API_KEY}",
            "Content-Type": "application/json",
        }
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    def _memory_from_response(self, data: Dict) -> HindsightMemory:
        return HindsightMemory(
            id=data.get("id", ""),
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
        client = await self._get_client()
        payload = {
            "query": query,
            "top_k": top_k,
            "min_score": min_score,
        }
        if filters:
            payload["filters"] = filters

        url = f"{self.base_url}/banks/{bank_id}/recall"
        try:
            resp = await client.post(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            memories = [self._memory_from_response(m) for m in data.get("memories", [])]
            return memories
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"Bank not found: {bank_id}, returning empty")
                return []
            logger.error(f"Hindsight recall failed: {e}")
            return []
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
        client = await self._get_client()
        payload = {
            "text": text,
            "metadata": metadata,
        }
        if merge_policy:
            payload["merge_policy"] = merge_policy

        url = f"{self.base_url}/banks/{bank_id}/memories"
        try:
            resp = await client.post(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return self._memory_from_response(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                await self._create_bank(bank_id)
                return await self.retain(bank_id, text, metadata, merge_policy)
            logger.error(f"Hindsight retain failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Hindsight retain error: {e}")
            raise

    async def _create_bank(self, bank_id: str):
        client = await self._get_client()
        url = f"{self.base_url}/banks"
        payload = {"id": bank_id}
        resp = await client.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        logger.info(f"Created bank: {bank_id}")

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