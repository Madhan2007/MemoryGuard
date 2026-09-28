"""
Hindsight Client Wrapper

Member 2 ownership.

Provides async interface to Hindsight persistent memory layer.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from .config import get_config, Config

logger = logging.getLogger(__name__)


class HindsightError(Exception):
    """Base exception for Hindsight errors."""
    pass


class HindsightUnavailableError(HindsightError):
    """Hindsight service unavailable."""
    pass


class HindsightTimeoutError(HindsightError):
    """Hindsight request timeout."""
    pass


class HindsightRateLimitError(HindsightError):
    """Hindsight rate limit exceeded."""
    pass


class BankNotFoundError(HindsightError):
    """Memory bank not found."""
    pass


class MergeConflictError(HindsightError):
    """Merge conflict during concurrent retain."""
    pass


class MergeStrategy(Enum):
    """Strategy for merging memories in Hindsight."""
    APPEND_PROVENANCE = "append_provenance"
    REPLACE = "replace"
    SYNTHESIZE = "synthesize"


@dataclass
class MergePolicy:
    """Merge policy instruction for Hindsight."""
    target_id: str
    strategy: MergeStrategy = MergeStrategy.APPEND_PROVENANCE


@dataclass
class Memory:
    """Memory record from Hindsight."""
    id: str
    text: str
    metadata: Dict[str, Any]
    score: Optional[float] = None


class HindsightClient:
    """
    Async client for Hindsight persistent memory layer.
    
    Provides recall, retain, and bank management operations.
    Supports mock mode for development without API access.
    """
    
    # Retry configuration
    RETRY_CONFIG = {
        "max_attempts": 3,
        "base_delay": 1.0,
        "max_delay": 10.0,
        "exponential_base": 2.0,
    }
    
    # Circuit breaker configuration
    CIRCUIT_BREAKER = {
        "failure_threshold": 5,
        "recovery_timeout": 30.0,
        "half_open_requests": 3,
    }
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        self.mock_mode = self.config.MOCK_HINDSIGHT
        
        # Circuit breaker state
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._circuit_state = "closed"  # closed, open, half-open
        
        # Mock storage for development
        self._mock_banks: Dict[str, Dict[str, Memory]] = {}
        
        # Initialize real SDK client if not mocking
        self._sdk = None
        if not self.mock_mode:
            self._init_sdk()
    
    def _init_sdk(self):
        """Initialize Hindsight SDK client."""
        # TODO: Replace with actual Hindsight SDK import
        # from hindsight import HindsightSDK
        # self._sdk = HindsightSDK(
        #     api_key=self.config.HINDSIGHT_API_KEY,
        #     base_url=self.config.HINDSIGHT_BASE_URL,
        # )
        logger.warning("Hindsight SDK not initialized - using mock mode")
        self.mock_mode = True
    
    def project_bank(self, deal_id: str) -> str:
        """Get project bank ID for deal."""
        return f"{self.config.HINDSIGHT_PROJECT_BANK_PREFIX}{deal_id}"
    
    def common_bank(self, rep_id: str) -> str:
        """Get common bank ID for rep."""
        return f"{self.config.HINDSIGHT_COMMON_BANK_PREFIX}{rep_id}"
    
    async def create_bank(self, bank_id: str) -> bool:
        """Create memory bank (idempotent)."""
        if self.mock_mode:
            if bank_id not in self._mock_banks:
                self._mock_banks[bank_id] = {}
            return True
        
        # TODO: Implement real SDK call
        # await self._sdk.create_bank(bank_id)
        return True
    
    async def recall(
        self,
        bank_id: str,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        min_score: float = 0.3
    ) -> List[Memory]:
        """
        Semantic recall from Hindsight memory bank.
        
        Args:
            bank_id: Hindsight bank identifier
            query: Search query text
            top_k: Maximum results to return
            filters: Optional metadata filters
            min_score: Minimum similarity score
            
        Returns:
            List of matching memories with scores
        """
        if self.mock_mode:
            return await self._mock_recall(bank_id, query, top_k)
        
        return await self._with_retry(
            self._sdk.recall,
            bank_id=bank_id,
            query=query,
            top_k=top_k,
            filters=filters,
            min_score=min_score
        )
    
    async def retain(
        self,
        bank_id: str,
        memory: str,
        metadata: Dict[str, Any],
        merge_policy: Optional[MergePolicy] = None
    ) -> Memory:
        """
        Store or update memory in Hindsight.
        
        Args:
            bank_id: Target bank identifier
            memory: Memory text content
            metadata: Memory metadata (includes MemoryGuard fields)
            merge_policy: Optional merge instruction for consolidation
            
        Returns:
            Created/updated memory record
        """
        if self.mock_mode:
            return await self._mock_retain(bank_id, memory, metadata, merge_policy)
        
        return await self._with_retry(
            self._sdk.retain,
            bank_id=bank_id,
            content=memory,
            metadata=metadata,
            merge_policy=merge_policy
        )
    
    async def get_memory(self, memory_id: str) -> Memory:
        """Get single memory by ID."""
        if self.mock_mode:
            for bank in self._mock_banks.values():
                if memory_id in bank:
                    return bank[memory_id]
            raise KeyError(f"Memory {memory_id} not found")
        
        # TODO: Implement real SDK call
        raise NotImplementedError("Real SDK get_memory not implemented")
    
    async def update_memory(self, memory_id: str, metadata: Dict[str, Any]) -> Memory:
        """Update memory metadata."""
        if self.mock_mode:
            for bank in self._mock_banks.values():
                if memory_id in bank:
                    bank[memory_id].metadata.update(metadata)
                    return bank[memory_id]
            raise KeyError(f"Memory {memory_id} not found")
        
        # TODO: Implement real SDK call
        raise NotImplementedError("Real SDK update_memory not implemented")
    
    # Circuit breaker methods
    def _check_circuit(self):
        """Check circuit breaker state."""
        if self._circuit_state == "open":
            if (asyncio.get_event_loop().time() - self._last_failure_time) > self.CIRCUIT_BREAKER["recovery_timeout"]:
                self._circuit_state = "half-open"
                logger.info("Circuit breaker entering half-open state")
            else:
                raise HindsightUnavailableError("Circuit breaker open")
    
    def _on_success(self):
        """Record successful call."""
        self._failure_count = 0
        self._circuit_state = "closed"
    
    def _on_failure(self):
        """Record failed call."""
        self._failure_count += 1
        self._last_failure_time = asyncio.get_event_loop().time()
        if self._failure_count >= self.CIRCUIT_BREAKER["failure_threshold"]:
            self._circuit_state = "open"
            logger.warning("Circuit breaker opened due to repeated failures")
    
    async def _with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic and circuit breaker."""
        self._check_circuit()
        
        for attempt in range(self.RETRY_CONFIG["max_attempts"]):
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except HindsightTimeoutError:
                if attempt == self.RETRY_CONFIG["max_attempts"] - 1:
                    self._on_failure()
                    raise
                delay = min(
                    self.RETRY_CONFIG["base_delay"] * (self.RETRY_CONFIG["exponential_base"] ** attempt),
                    self.RETRY_CONFIG["max_delay"]
                )
                logger.warning(f"Hindsight timeout, retrying in {delay}s", attempt=attempt + 1)
                await asyncio.sleep(delay)
            except HindsightRateLimitError:
                self._on_failure()
                await asyncio.sleep(5.0)
                continue
            except Exception as e:
                self._on_failure()
                # Don't retry on unknown errors
                logger.error(f"Hindsight error: {e}")
                raise HindsightUnavailableError(f"Hindsight operation failed: {e}")
        
        raise HindsightUnavailableError("Max retries exceeded")
    
    # Mock implementations
    async def _mock_recall(self, bank_id: str, query: str, top_k: int) -> List[Memory]:
        """Mock recall for development."""
        if bank_id not in self._mock_banks:
            return []
        
        memories = list(self._mock_banks[bank_id].values())
        # Simple text matching for mock
        query_lower = query.lower()
        matched = [
            m for m in memories 
            if query_lower in m.text.lower() or any(query_lower in str(v).lower() for v in m.metadata.values())
        ]
        return matched[:top_k]
    
    async def _mock_retain(
        self, 
        bank_id: str, 
        memory: str, 
        metadata: Dict[str, Any],
        merge_policy: Optional[MergePolicy] = None
    ) -> Memory:
        """Mock retain for development."""
        if bank_id not in self._mock_banks:
            self._mock_banks[bank_id] = {}
        
        import uuid
        mem_id = metadata.get("audit_id", f"mock-{uuid.uuid4().hex[:8]}")
        
        # Handle merge policy
        if merge_policy and merge_policy.target_id in self._mock_banks[bank_id]:
            # Merge into existing
            existing = self._mock_banks[bank_id][merge_policy.target_id]
            existing.text = memory  # Simplified: replace text
            existing.metadata.update(metadata)
            existing.metadata["frequency"] = merge_policy.strategy == "append_provenance" and existing.metadata.get("frequency", 1) + 1 or 1
            return existing
        
        mem = Memory(
            id=mem_id,
            text=memory,
            metadata=metadata
        )
        self._mock_banks[bank_id][mem_id] = mem
        return mem
    
    def clear_mock_data(self):
        """Clear all mock data (for testing)."""
        self._mock_banks.clear()


__all__ = [
    "HindsightClient",
    "Memory",
    "MergePolicy",
    "MergeStrategy",
    "HindsightError",
    "HindsightUnavailableError",
    "HindsightTimeoutError",
    "HindsightRateLimitError",
    "BankNotFoundError",
    "MergeConflictError",
]