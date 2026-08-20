from contextlib import contextmanager
from time import perf_counter
import logging
log=logging.getLogger("trace")
@contextmanager
def span(name:str, **attrs):
    started=perf_counter(); error=None
    try: yield
    except Exception as exc: error=type(exc).__name__; raise
    finally: log.info("span=%s latency_ms=%.2f error=%s attrs=%s",name,(perf_counter()-started)*1000,error,attrs)
