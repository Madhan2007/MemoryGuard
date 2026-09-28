# Member 2 - Backend Design

## Status: PLANNED

## Agent Loop Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AgentLoop.process_turn()                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. RECALL PHASE                                                │
│     project_memories = hindsight.recall(project_bank, query)   │
│     common_memories = hindsight.recall(common_bank, query)     │
│     relevant_memories = merge_and_rank(project, common)        │
│                                                                  │
│  2. CONTEXT BUILD                                               │
│     system_prompt = build_system_prompt(relevant_memories)     │
│     messages = [system_prompt] + conversation_history          │
│                                                                  │
│  3. GENERATION PHASE                                            │
│     response = groq.call_main_llm(messages)                    │
│     candidate_memories = extract_candidates(response)          │
│                                                                  │
│  4. GOVERNANCE PHASE (per candidate)                            │
│     for candidate in candidate_memories:                       │
│         decision = memoryguard.verify(                         │
│             candidate, source_text, context, scope             │
│         )                                                      │
│         if decision.decision in [RETAIN, UPDATE, MERGE]:       │
│             hindsight.retain(decision)                         │
│                                                                  │
│  5. RESPONSE                                                    │
│     return AgentResponse(                                      │
│         response_text=response,                                │
│         candidate_memories=candidates,                         │
│         memory_decisions=decisions,                            │
│         recalled_memories=relevant_memories                    │
│     )                                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. Configuration (`config.py`)

```python
class Config(BaseSettings):
    # LLM
    GROQ_API_KEY: str
    MAIN_MODEL: str = "openai/gpt-oss-20b"
    VERIFIER_MODEL: str = "openai/gpt-oss-120b"
    MAIN_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    VERIFIER_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    MAIN_MODEL_TEMPERATURE: float = 0.3
    VERIFIER_MODEL_TEMPERATURE: float = 0.1
    MAIN_MODEL_MAX_TOKENS: int = 2048
    VERIFIER_MODEL_MAX_TOKENS: int = 1024
    
    # Hindsight
    HINDSIGHT_API_KEY: str
    HINDSIGHT_BASE_URL: str
    HINDSIGHT_PROJECT_BANK_PREFIX: str = "memoryguard-project-"
    HINDSIGHT_COMMON_BANK_PREFIX: str = "memoryguard-common-"
    
    # App
    LOG_LEVEL: str = "INFO"
    STREAMLIT_PORT: int = 8501
    
    # Feature flags
    MOCK_HINDSIGHT: bool = False
    MOCK_LLM: bool = False
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Singleton
_config: Optional[Config] = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
```

### 2. Groq Client (`groq_client.py`)

```python
class GroqClient:
    def __init__(self, config: Config):
        self.config = config
        self.main_client = AsyncGroq(
            api_key=config.GROQ_API_KEY,
            base_url=config.MAIN_MODEL_BASE_URL
        )
        self.verifier_client = AsyncGroq(
            api_key=config.GROQ_API_KEY,
            base_url=config.VERIFIER_MODEL_BASE_URL
        )
    
    async def call_main_llm(self, messages: List[Dict]) -> str:
        if self.config.MOCK_LLM:
            return self._mock_response(messages)
        
        for model in self._main_model_fallbacks():
            try:
                response = await self.main_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=self.config.MAIN_MODEL_TEMPERATURE,
                    max_tokens=self.config.MAIN_MODEL_MAX_TOKENS,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                continue
        raise AllModelsFailed("No main models available")
    
    async def call_verifier_llm(self, messages: List[Dict]) -> VerificationResponse:
        if self.config.MOCK_LLM:
            return self._mock_verification()
        
        for model in self._verifier_model_fallbacks():
            try:
                response = await self.verifier_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=self.config.VERIFIER_MODEL_TEMPERATURE,
                    max_tokens=self.config.VERIFIER_MODEL_MAX_TOKENS,
                    response_format={"type": "json_object"},
                )
                return parse_verification(response.choices[0].message.content)
            except Exception as e:
                logger.warning(f"Verifier {model} failed: {e}")
                continue
        raise AllModelsFailed("No verifier models available")
```

### 3. Hindsight Client (`hindsight_client.py`)

```python
class HindsightClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = HindsightSDK(
            api_key=config.HINDSIGHT_API_KEY,
            base_url=config.HINDSIGHT_BASE_URL
        )
    
    def project_bank(self, deal_id: str) -> str:
        return f"{self.config.HINDSIGHT_PROJECT_BANK_PREFIX}{deal_id}"
    
    def common_bank(self, rep_id: str) -> str:
        return f"{self.config.HINDSIGHT_COMMON_BANK_PREFIX}{rep_id}"
    
    async def recall(
        self,
        bank_id: str,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict] = None,
        min_score: float = 0.3
    ) -> List[Memory]:
        if self.config.MOCK_HINDSIGHT:
            return self._mock_recall(bank_id, query)
        
        # Retry with circuit breaker
        return await self._with_retry(
            self.client.recall,
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
        metadata: MemoryMetadata,
        merge_policy: Optional[MergePolicy] = None
    ) -> Memory:
        if self.config.MOCK_HINDSIGHT:
            return self._mock_retain(bank_id, memory, metadata)
        
        return await self._with_retry(
            self.client.retain,
            bank_id=bank_id,
            content=memory,
            metadata=metadata.to_hindsight_dict(),
            merge_policy=merge_policy
        )
```

### 4. Agent Harness (`agent_harness.py`)

```python
class AgentLoop:
    def __init__(
        self,
        hindsight: HindsightClient,
        groq: GroqClient,
        memoryguard: MemoryGuard,
        session_store: SessionStore
    ):
        self.hindsight = hindsight
        self.groq = groq
        self.memoryguard = memoryguard
        self.sessions = session_store
    
    async def process_turn(
        self,
        user_input: str,
        deal_id: str,
        rep_id: str
    ) -> AgentResponse:
        session = await self.sessions.get_or_create(deal_id, rep_id)
        session.add_turn("user", user_input)
        
        # 1. Recall
        query = self._build_recall_query(user_input, session)
        project_memories = await self.hindsight.recall(
            self.hindsight.project_bank(deal_id), query
        )
        common_memories = await self.hindsight.recall(
            self.hindsight.common_bank(rep_id), query
        )
        relevant = self._merge_and_rank(project_memories, common_memories)
        
        # 2. Context
        messages = self._build_messages(session, relevant)
        
        # 3. Generate
        response = await self.groq.call_main_llm(messages)
        candidates = self._extract_candidates(response, session)
        
        # 4. Governance
        decisions = []
        for candidate in candidates:
            context = self._build_verification_context(candidate, session, deal_id, rep_id)
            scope = await self.memoryguard.determine_scope(candidate, context)
            decision = await self.memoryguard.verify(candidate, session.last_user_text, context, scope)
            decisions.append(decision)
            
            if decision.decision in [DecisionType.RETAIN, DecisionType.UPDATE, DecisionType.MERGE]:
                await self._persist_decision(decision, deal_id, rep_id)
        
        # 5. Update session
        session.add_turn("assistant", response)
        
        return AgentResponse(
            response_text=response,
            candidate_memories=candidates,
            memory_decisions=decisions,
            recalled_memories=relevant,
            turn_metadata=TurnMetadata(
                turn_id=session.turn_count,
                latency_ms=..., 
                tokens_used=...
            )
        )
```

### 5. Session (`session.py`)

```python
class Session:
    def __init__(self, deal_id: str, rep_id: str):
        self.deal_id = deal_id
        self.rep_id = rep_id
        self.turns: List[Turn] = []
        self.turn_count = 0
    
    def add_turn(self, role: str, content: str):
        self.turns.append(Turn(role=role, content=content, turn_id=self.turn_count))
        self.turn_count += 1
    
    def get_history(self, max_turns: int = 10) -> List[Turn]:
        return self.turns[-max_turns:]
    
    @property
    def last_user_text(self) -> str:
        for turn in reversed(self.turns):
            if turn.role == "user":
                return turn.content
        return ""
```

### 6. Logging (`logger.py`)

```python
def setup_logging(level: str = "INFO"):
    import structlog
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
        handlers=[RichHandler(rich_tracebacks=True)]
    )

def get_logger(name: str):
    return structlog.get_logger(name)

# Usage
logger = get_logger(__name__)
logger.info("turn_processed", deal_id="acme", rep_id="rep-1", turn=5, latency_ms=234)
```

## Error Handling Strategy

| Component | Strategy |
|-----------|----------|
| Hindsight recall | Retry 3x, then empty list (graceful degradation) |
| Hindsight retain | Retry 3x, queue for background sync |
| Main LLM | Fallback model chain, then cached response |
| Verifier LLM | Fallback model chain, then rule-based verification |
| MemoryGuard | Deterministic fallback rules |
| Session | In-memory with periodic persistence |

---

**Status: PLANNED** — Implementation follows this design.