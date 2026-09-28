"""
Session Management

Member 2 ownership.

Manages conversation state and history.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from abc import ABC, abstractmethod


@dataclass
class Turn:
    """Single conversation turn."""
    role: str  # "user" or "assistant"
    content: str
    turn_id: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """Conversation session for a deal/rep pair."""
    deal_id: str
    rep_id: str
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    turns: List[Turn] = field(default_factory=list)
    turn_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_turn(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a turn to the conversation."""
        self.turn_count += 1
        turn = Turn(
            role=role,
            content=content,
            turn_id=self.turn_count,
            metadata=metadata or {}
        )
        self.turns.append(turn)
        self.updated_at = datetime.utcnow()
    
    def get_history(self, max_turns: int = 10) -> List[Turn]:
        """Get recent conversation history."""
        return self.turns[-max_turns:]
    
    @property
    def last_user_text(self) -> str:
        """Get last user message."""
        for turn in reversed(self.turns):
            if turn.role == "user":
                return turn.content
        return ""
    
    @property
    def last_assistant_text(self) -> str:
        """Get last assistant message."""
        for turn in reversed(self.turns):
            if turn.role == "assistant":
                return turn.content
        return ""


class SessionStore(ABC):
    """Abstract session storage interface."""
    
    @abstractmethod
    async def get_or_create(self, deal_id: str, rep_id: str) -> Session:
        """Get existing session or create new one."""
        pass
    
    @abstractmethod
    async def get(self, deal_id: str, rep_id: str) -> Optional[Session]:
        """Get session if exists."""
        pass
    
    @abstractmethod
    async def save(self, session: Session) -> None:
        """Save session."""
        pass
    
    @abstractmethod
    async def delete(self, deal_id: str, rep_id: str) -> None:
        """Delete session."""
        pass


class InMemorySessionStore(SessionStore):
    """In-memory session storage for development."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
    
    def _key(self, deal_id: str, rep_id: str) -> str:
        return f"{deal_id}:{rep_id}"
    
    async def get_or_create(self, deal_id: str, rep_id: str) -> Session:
        key = self._key(deal_id, rep_id)
        if key not in self._sessions:
            self._sessions[key] = Session(deal_id=deal_id, rep_id=rep_id)
        return self._sessions[key]
    
    async def get(self, deal_id: str, rep_id: str) -> Optional[Session]:
        key = self._key(deal_id, rep_id)
        return self._sessions.get(key)
    
    async def save(self, session: Session) -> None:
        key = self._key(session.deal_id, session.rep_id)
        self._sessions[key] = session
    
    async def delete(self, deal_id: str, rep_id: str) -> None:
        key = self._key(deal_id, rep_id)
        if key in self._sessions:
            del self._sessions[key]


class PersistentSessionStore(SessionStore):
    """Persistent session storage (future: Redis/DB)."""
    
    def __init__(self):
        pass
    
    async def get_or_create(self, deal_id: str, rep_id: str) -> Session:
        raise NotImplementedError("Persistent store not implemented")
    
    async def get(self, deal_id: str, rep_id: str) -> Optional[Session]:
        raise NotImplementedError("Persistent store not implemented")
    
    async def save(self, session: Session) -> None:
        raise NotImplementedError("Persistent store not implemented")
    
    async def delete(self, deal_id: str, rep_id: str) -> None:
        raise NotImplementedError("Persistent store not implemented")


__all__ = [
    "Turn",
    "Session",
    "SessionStore",
    "InMemorySessionStore",
    "PersistentSessionStore",
]