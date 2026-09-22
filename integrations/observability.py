"""Privacy-minimized GoreeCloud Observability v1 signal construction.

This module adopts the producer contract at an exact authoritative revision. It
constructs contract-shaped source evidence only; it does not publish telemetry,
authenticate to an Observability service, or establish production monitoring.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

OBSERVABILITY_CONTRACT_REPOSITORY = "GoreeCloud/observability"
OBSERVABILITY_CONTRACT_REVISION = "a7f6a65f442d3e517baddbe7b6ce7c250d142c8c"
OBSERVABILITY_CONTRACT_ID = (
    "https://goreecloud.com/contracts/observability/operational-signal/v1"
)
MANAGER_COMPONENT_ID = "goreecloud-manager"
MANAGER_SIGNAL_SOURCE = "goreecloud-manager"

OBSERVABILITY_STATES = frozenset(
    {
        "healthy",
        "degraded",
        "failed",
        "unavailable",
        "unknown",
        "stale",
        "partially_observed",
        "not_monitored",
        "not_applicable",
    }
)

_SENSITIVE_ATTRIBUTE_TOKENS = (
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "credential",
    "password",
    "passwd",
    "private_key",
    "secret",
    "token",
)


def _nonempty_string(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _utc_timestamp(value: object, *, field: str) -> str:
    if not isinstance(value, datetime):
        raise ValueError(f"{field} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _looks_sensitive(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_").replace(" ", "_")
    return any(token in normalized for token in _SENSITIVE_ATTRIBUTE_TOKENS)


def _validate_attribute_value(value: Any, *, path: str) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path} must be JSON-finite")
        return value
    if isinstance(value, Mapping):
        validated: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            key = _nonempty_string(raw_key, field=f"{path} key")
            if _looks_sensitive(key):
                raise ValueError(f"{path}.{key} is not allowed in Observability attributes")
            validated[key] = _validate_attribute_value(raw_value, path=f"{path}.{key}")
        return validated
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [
            _validate_attribute_value(item, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        ]
    raise ValueError(f"{path} contains a non-JSON-safe value")


def build_operational_signal(
    *,
    signal_id: str,
    signal_type: str,
    state: str,
    observed_at: datetime,
    collected_at: datetime | None = None,
    ttl_seconds: int = 60,
    correlation_id: str | None = None,
    attributes: Mapping[str, Any] | None = None,
    collection_gaps: Sequence[str] = (),
) -> dict[str, Any]:
    """Build one Manager-owned signal matching the Observability v1 contract.

    Callers must supply explicit state. Missing evidence must be represented as
    ``unknown``/``unavailable``/another truthful contract state; this helper never
    turns absence into ``healthy``.
    """

    signal_id = _nonempty_string(signal_id, field="signal_id")
    signal_type = _nonempty_string(signal_type, field="signal_type")
    state = _nonempty_string(state, field="state")
    if state not in OBSERVABILITY_STATES:
        raise ValueError(f"unsupported Observability state: {state}")

    if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int):
        raise ValueError("ttl_seconds must be an integer")
    if not 1 <= ttl_seconds <= 86400:
        raise ValueError("ttl_seconds must be between 1 and 86400")

    observed = _utc_timestamp(observed_at, field="observed_at")
    collected = _utc_timestamp(
        collected_at if collected_at is not None else observed_at,
        field="collected_at",
    )

    payload: dict[str, Any] = {
        "signal_id": signal_id,
        "component_id": MANAGER_COMPONENT_ID,
        "source": MANAGER_SIGNAL_SOURCE,
        "signal_type": signal_type,
        "state": state,
        "observed_at": observed,
        "collected_at": collected,
        "ttl_seconds": ttl_seconds,
    }

    if correlation_id is not None:
        payload["correlation_id"] = _nonempty_string(
            correlation_id, field="correlation_id"
        )

    if attributes is not None:
        payload["attributes"] = _validate_attribute_value(
            attributes, path="attributes"
        )

    gaps = [
        _nonempty_string(gap, field="collection_gaps item")
        for gap in collection_gaps
    ]
    if gaps:
        payload["collection_gaps"] = gaps

    return payload
