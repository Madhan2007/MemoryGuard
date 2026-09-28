# Security Considerations

## Status: PLANNED

## API Keys & Secrets

### Environment Variables
- All secrets in `.env` (never committed)
- `.env.example` provides template
- Git ignores `.env*` patterns

### Runtime Handling
```python
# src/integrations/config.py
class Config(BaseSettings):
    GROQ_API_KEY: str
    HINDSIGHT_API_KEY: str
    
    class Config:
        env_file = ".env"
        # No default values for secrets
```

### Logging Restrictions
- **Never log** API keys, tokens, or secrets
- Structured logging excludes sensitive fields
- Audit logs contain decision metadata, not credentials

## Sensitive Memory Handling

### PII Detection (Rule R25)
- Detect: emails, phones, SSN, credit cards, names
- Configurable detection patterns
- Flag for review, don't auto-reject (business context may require)

### PII Redaction (Rule R26)
- Stored memory: `[REDACTED]` placeholder
- Audit trail: Original quote preserved (encrypted at rest)
- UI displays: Redacted version by default

### Compliance Tagging (Rule R27)
- Auto-tag: SOC2, GDPR, HIPAA, PCI, SOX
- Retention policies per tag
- Export controls for compliance memories

## Audit Trail

### Immutability (Rule R28)
- Audit records append-only
- Cryptographic hash chain (future)
- Tamper-evident storage

### Audit Contents
```json
{
  "audit_id": "uuid",
  "timestamp": "ISO8601",
  "actor": "memoryguard",
  "action": "RETAIN|MERGE|REJECT|UPDATE",
  "memory_id": "uuid",
  "decision": {...},
  "provenance": {...},
  "hash": "sha256(previous_hash + current_record)"
}
```

## Memory Deletion / Forgetting (Future)

### Requirements
- Right to be forgotten (GDPR)
- Deal closure cleanup
- Rep offboarding

### Implementation (Post-MVP)
- Soft delete with tombstone
- Hard delete after retention period
- Cascade to Hindsight banks
- Audit log retention separate

## Network Security

### Hindsight Communication
- HTTPS only (enforced in config)
- Certificate validation
- Request signing (if supported)

### LLM Provider
- Groq/OpenAI-compatible over HTTPS
- API key in header (not URL)
- Request/response logging excludes auth headers

## Development Safety

### Debug Mode
```bash
DEBUG=true
MOCK_HINDSIGHT=true
MOCK_LLM=true
```
- Mock modes for development without API calls
- Never use real credentials in mock mode

### Test Data
- Synthetic scenarios only
- No real customer data in repo
- `src/data/scenarios/` contains fictional companies

## Incident Response

### Key Compromise
1. Rotate API keys immediately
2. Invalidate Hindsight tokens
3. Audit recent memory writes
4. Notify team

### Data Breach
1. Assess scope (which banks affected)
2. Notify stakeholders
3. Implement containment
4. Document lessons learned

---

**Status: PLANNED** — Implementation in `src/integrations/config.py` and `src/memory/security.py` (future).