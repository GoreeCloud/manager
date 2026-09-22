"""Bounded GoreeCloud Policy v1 request and decision contract helpers.

This module adopts the Policy request/decision contracts at an exact authoritative
revision. It constructs evaluation-request data and validates returned decision
evidence only. It does not call a Policy runtime, distribute policy, enforce a
decision, mutate Manager state, or turn an ``allow`` decision into Manager
authorization.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

POLICY_CONTRACT_REPOSITORY = "GoreeCloud/policy"
POLICY_CONTRACT_REVISION = "46071886da37a6566b69cc923005eef64cce2bcc"
POLICY_EVALUATION_REQUEST_CONTRACT_ID = (
    "https://goreecloud.com/contracts/policy/evaluation-request/v1"
)
POLICY_DECISION_CONTRACT_ID = "https://goreecloud.com/contracts/policy/decision/v1"

POLICY_DECISIONS = frozenset(
    {
        "allow",
        "deny",
        "conditional",
        "defer",
        "indeterminate",
        "error",
    }
)

_REQUEST_REQUIRED_FIELDS = (
    "policy_id",
    "policy_version",
    "authority",
    "subject",
    "resource",
    "action",
)
_DECISION_REQUIRED_FIELDS = (
    "decision",
    "policy_id",
    "policy_version",
    "authority",
    "subject",
    "resource",
    "action",
    "reason",
    "matched_rule_ids",
    "obligations",
    "evaluated_at",
    "fresh",
)
_SENSITIVE_CONTEXT_TOKENS = (
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


def _looks_sensitive(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_").replace(" ", "_")
    return any(token in normalized for token in _SENSITIVE_CONTEXT_TOKENS)


def _validate_json_value(value: Any, *, path: str) -> Any:
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
                raise ValueError(f"{path}.{key} is not allowed in Policy context")
            validated[key] = _validate_json_value(raw_value, path=f"{path}.{key}")
        return validated
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [
            _validate_json_value(item, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        ]
    raise ValueError(f"{path} contains a non-JSON-safe value")


def _validated_string_list(value: object, *, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list of strings")
    return [
        _nonempty_string(item, field=f"{field} item")
        for item in value
    ]


def _validated_timestamp(value: object, *, field: str) -> str:
    text = _nonempty_string(value, field=field)
    parse_value = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(parse_value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone offset")
    return text


def build_evaluation_request(
    *,
    policy_id: str,
    policy_version: str,
    authority: str,
    subject: str,
    resource: str,
    action: str,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one exact-shape Policy v1 evaluation request.

    Context is optional and privacy-minimized before construction. This function
    performs no network request and introduces no authentication material.
    """

    payload: dict[str, Any] = {
        "policy_id": _nonempty_string(policy_id, field="policy_id"),
        "policy_version": _nonempty_string(policy_version, field="policy_version"),
        "authority": _nonempty_string(authority, field="authority"),
        "subject": _nonempty_string(subject, field="subject"),
        "resource": _nonempty_string(resource, field="resource"),
        "action": _nonempty_string(action, field="action"),
    }

    if context is not None:
        if not isinstance(context, Mapping):
            raise ValueError("context must be an object")
        payload["context"] = _validate_json_value(context, path="context")

    return payload


def validate_policy_decision(
    decision: Mapping[str, Any],
    *,
    expected_request: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate Policy v1 decision evidence and optional request provenance.

    A validated ``allow`` value remains Policy decision evidence only. Callers
    must not treat this helper as Manager authorization or execution authority.
    """

    if not isinstance(decision, Mapping):
        raise ValueError("decision must be an object")

    keys = set(decision)
    required = set(_DECISION_REQUIRED_FIELDS)
    if keys != required:
        missing = sorted(required - keys)
        extra = sorted(keys - required)
        raise ValueError(
            f"decision must contain the exact Policy v1 fields; missing={missing}, extra={extra}"
        )

    decision_value = _nonempty_string(decision["decision"], field="decision")
    if decision_value not in POLICY_DECISIONS:
        raise ValueError(f"unsupported Policy decision: {decision_value}")

    validated: dict[str, Any] = {
        "decision": decision_value,
        "policy_id": _nonempty_string(decision["policy_id"], field="policy_id"),
        "policy_version": _nonempty_string(
            decision["policy_version"], field="policy_version"
        ),
        "authority": _nonempty_string(decision["authority"], field="authority"),
        "subject": _nonempty_string(decision["subject"], field="subject"),
        "resource": _nonempty_string(decision["resource"], field="resource"),
        "action": _nonempty_string(decision["action"], field="action"),
        "reason": _nonempty_string(decision["reason"], field="reason"),
        "matched_rule_ids": _validated_string_list(
            decision["matched_rule_ids"], field="matched_rule_ids"
        ),
        "obligations": _validated_string_list(
            decision["obligations"], field="obligations"
        ),
        "evaluated_at": _validated_timestamp(
            decision["evaluated_at"], field="evaluated_at"
        ),
    }

    fresh = decision["fresh"]
    if not isinstance(fresh, bool):
        raise ValueError("fresh must be a boolean")
    validated["fresh"] = fresh

    if expected_request is not None:
        if not isinstance(expected_request, Mapping):
            raise ValueError("expected_request must be an object")
        for field in _REQUEST_REQUIRED_FIELDS:
            if field not in expected_request:
                raise ValueError(f"expected_request is missing {field}")
            expected = _nonempty_string(expected_request[field], field=f"expected {field}")
            if validated[field] != expected:
                raise ValueError(f"Policy decision provenance mismatch for {field}")

    return validated
