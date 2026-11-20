"""
Logging for the engine.

One rotating file, logs/engine.log (1 MB, 5 old files kept), plus the console.
Set LOG_LEVEL (default INFO) and ENGINE_LOG_DIR (default logs/) in the environment
to change that.

What is logged: AI calls (what for, how long, token counts, why one failed), web
requests (method, path, status, time, user id, case id) and unhandled errors with a
traceback. What is NOT logged: prompts, answers, case texts, form contents or query
strings. The cases are the owner's own words and can be sensitive, so the log only
says what happened, not what was written.
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s %(message)s"
_configured = False
_file_handler = None


def _setup():
    global _configured, _file_handler
    if _configured:
        return
    root = logging.getLogger("engine")
    root.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())
    root.propagate = False
    log_dir = Path(os.environ.get("ENGINE_LOG_DIR", "logs"))
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        _file_handler = RotatingFileHandler(log_dir / "engine.log", maxBytes=1_000_000,
                                            backupCount=5, encoding="utf-8")
        _file_handler.setFormatter(logging.Formatter(_FORMAT))
        root.addHandler(_file_handler)
    except OSError as e:  # logging must never stop the app from starting
        print(f"  [log] could not open the log file: {e}")
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)-7s %(name)s %(message)s"))
    root.addHandler(console)
    _configured = True


def get_logger(name: str = "app") -> logging.Logger:
    """A logger under the 'engine' tree, e.g. get_logger('ai') -> 'engine.ai'."""
    _setup()
    return logging.getLogger(f"engine.{name}")


def attach_file_handler(logger: logging.Logger) -> None:
    """Send another logger's records (e.g. Flask's, which carries tracebacks) to the file."""
    _setup()
    if _file_handler is not None and _file_handler not in logger.handlers:
        logger.addHandler(_file_handler)


def log_ai(log: logging.Logger, purpose: str, started: float, response=None, error=None, **extra) -> None:
    """One line per AI call: what for, how long, token counts. Never the content."""
    parts = [f"ai purpose={purpose}", f"ms={int((time.time() - started) * 1000)}"]
    parts += [f"{k}={v}" for k, v in extra.items() if v not in (None, "")]
    if error is not None:
        parts += ["ok=0", f"error={type(error).__name__}:{str(error)[:200]!r}"]
        log.warning(" ".join(parts))
        return
    usage = getattr(response, "usage", None)
    details = getattr(usage, "completion_tokens_details", None)
    parts += [
        "ok=1",
        f"prompt_tokens={getattr(usage, 'prompt_tokens', '?')}",
        f"completion_tokens={getattr(usage, 'completion_tokens', '?')}",
        f"reasoning_tokens={getattr(details, 'reasoning_tokens', '?')}",
        f"finish={getattr(response.choices[0], 'finish_reason', '?')}",
    ]
    log.info(" ".join(parts))
