"""
Structured Logging

Member 2 ownership.

Provides structured JSON logging with Rich console output.
"""

import logging
import structlog
from typing import Any, Dict
from rich.logging import RichHandler


def setup_logging(level: str = "INFO", json_format: bool = True) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_format: If True, output JSON; if False, use Rich console
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    if json_format:
        # JSON structured logging for production
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
            level=log_level,
        )
    else:
        # Rich console logging for development
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer(colors=True)
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        logging.basicConfig(
            format="%(message)s",
            level=log_level,
            handlers=[RichHandler(rich_tracebacks=True, markup=True)]
        )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class LogContext:
    """Context manager for adding structured context to logs."""
    
    def __init__(self, logger: structlog.BoundLogger, **context):
        self.logger = logger
        self.context = context
        self.bound_logger = None
    
    def __enter__(self):
        self.bound_logger = self.logger.bind(**self.context)
        return self.bound_logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def log_with_context(logger: structlog.BoundLogger, **context) -> LogContext:
    """Create a context manager for structured logging."""
    return LogContext(logger, **context)


# Convenience function for common logging patterns
def log_turn_started(logger: structlog.BoundLogger, deal_id: str, rep_id: str, turn: int):
    logger.info("turn_started", deal_id=deal_id, rep_id=rep_id, turn=turn)


def log_turn_completed(
    logger: structlog.BoundLogger, 
    deal_id: str, 
    rep_id: str, 
    turn: int, 
    latency_ms: float,
    candidates: int,
    decisions: int
):
    logger.info(
        "turn_completed",
        deal_id=deal_id,
        rep_id=rep_id,
        turn=turn,
        latency_ms=round(latency_ms, 2),
        candidates=candidates,
        decisions=decisions,
    )


def log_memory_decision(
    logger: structlog.BoundLogger,
    decision_type: str,
    memory_text: str,
    confidence: float,
    scope: str,
    audit_id: str
):
    logger.info(
        "memory_decision",
        decision_type=decision_type,
        memory_text=memory_text[:100],
        confidence=round(confidence, 3),
        scope=scope,
        audit_id=audit_id,
    )


def log_hindsight_operation(
    logger: structlog.BoundLogger,
    operation: str,
    bank_id: str,
    success: bool,
    latency_ms: float,
    error: str = None
):
    logger.info(
        "hindsight_operation",
        operation=operation,
        bank_id=bank_id,
        success=success,
        latency_ms=round(latency_ms, 2),
        error=error,
    )


def log_llm_call(
    logger: structlog.BoundLogger,
    role: str,  # "main" or "verifier"
    model: str,
    success: bool,
    latency_ms: float,
    tokens: int = 0,
    error: str = None
):
    logger.info(
        "llm_call",
        role=role,
        model=model,
        success=success,
        latency_ms=round(latency_ms, 2),
        tokens=tokens,
        error=error,
    )


def log_error_with_context(
    logger: structlog.BoundLogger,
    error: Exception,
    **context
):
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        **context
    )


__all__ = [
    "setup_logging",
    "get_logger",
    "log_with_context",
    "log_turn_started",
    "log_turn_completed",
    "log_memory_decision",
    "log_hindsight_operation",
    "log_llm_call",
    "log_error_with_context",
]