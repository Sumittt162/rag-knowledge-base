import structlog
import logging
from src.config import settings

def configure_logging():
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.log_level),
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
    )

def get_logger(name: str):
    return structlog.get_logger(name)

configure_logging()