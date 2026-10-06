"""Bounded provider diagnostics: never accept exception or request contents."""

import json
import logging

logger = logging.getLogger(__name__)


def log_failure(provider: str, operation: str, failure: str, http_status: int | None = None) -> None:
    event = {
        "event": "provider_failure",
        "provider": provider if provider in {"openai", "devexpert"} else "unknown",
        "operation": operation if operation in {"chat", "stt"} else "unknown",
        "failure": failure if failure in {
            "http", "network", "timeout", "invalid_json", "missing_output",
            "missing_credential", "invalid_provider",
        } else "unknown",
    }
    if type(http_status) is int and 100 <= http_status <= 599:
        event["http_status"] = http_status
    logger.warning(json.dumps(event, sort_keys=True))
