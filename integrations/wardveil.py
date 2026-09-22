"""Bounded source validation for Wardveil Security State v2 evidence.

This module validates Wardveil-authored security-state records against the
source contract pinned below. It performs no network access, authenticates no
producer, executes no security control, and grants no Manager authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping

WARDVEIL_CONTRACT_REPOSITORY = "GoreeCloud/wardveil"
WARDVEIL_CONTRACT_REVISION = "9b41040ed48037451e660e860908316732384282"
WARDVEIL_SECURITY_STATE_CONTRACT_ID = "urn:goreecloud:wardveil:security-state:0.2.0"
WARDVEIL_SECURITY_STATE_VERSION = "0.2.0"

SECURITY_STATES = {
    "protected",
    "at_risk",
    "action_required",
    "unknown",
    "not_covered",
    "degraded",
    "contained",
    "recovering",
    "reconciliation_required",
}
COVERAGE_STATES = {"covered", "partial", "not_covered", "unknown", "stale", "degraded"}
EVIDENCE_STATES = {"current", "stale", "unavailable", "unverified"}
SCOPE_KINDS = {
    "account",
    "application",
    "service",
    "device",
    "network",
    "data",
    "control",
    "platform",
    "other",
}
LEGACY_PRESENTATION_STATES = {"protected", "attention", "degraded", "unknown", "not_applicable"}

_TOP_LEVEL_FIELDS = {
    "contract_version",
    "record_type",
    "record_id",
    "scope",
    "authority",
    "state",
    "coverage",
    "evidence",
    "claim",
    "explanation",
}


def _mapping(value: Any, field: str, allowed: set[str], required: set[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    keys = set(value)
    if not required <= keys:
        raise ValueError(f"{field} is missing required fields: {sorted(required - keys)}")
    if not keys <= allowed:
        raise ValueError(f"{field} contains unsupported fields: {sorted(keys - allowed)}")
    return value


def _text(value: Any, field: str, *, maximum: int) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or len(value) > maximum:
        raise ValueError(f"{field} must be non-empty bounded canonical text")
    if any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value):
        raise ValueError(f"{field} must not contain control characters")
    return value


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be an RFC3339/ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an RFC3339/ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return parsed


def _string_list(
    value: Any,
    field: str,
    *,
    minimum_items: int = 0,
    maximum_items: int,
    maximum_length: int,
) -> list[str]:
    if not isinstance(value, list) or not minimum_items <= len(value) <= maximum_items:
        raise ValueError(f"{field} must be an array with {minimum_items}..{maximum_items} items")
    return [_text(item, f"{field}[{index}]", maximum=maximum_length) for index, item in enumerate(value)]


def validate_security_state(
    record: Mapping[str, Any],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate a Wardveil Security State v2 record and return a detached copy.

    Validation is deliberately evidence-only. A valid record is not an
    authorization result and does not prove that the sender is Wardveil; live
    producer authentication remains a separate acceptance gate.
    """

    value = _mapping(record, "record", _TOP_LEVEL_FIELDS, _TOP_LEVEL_FIELDS)

    if value["contract_version"] != WARDVEIL_SECURITY_STATE_VERSION:
        raise ValueError("unsupported Wardveil security-state contract_version")
    if value["record_type"] != "security_state":
        raise ValueError("record_type must be security_state")
    _text(value["record_id"], "record_id", maximum=160)

    scope = _mapping(value["scope"], "scope", {"kind", "id"}, {"kind", "id"})
    if scope["kind"] not in SCOPE_KINDS:
        raise ValueError("unsupported scope kind")
    _text(scope["id"], "scope.id", maximum=128)

    authority = _mapping(
        value["authority"],
        "authority",
        {"system", "control", "authoritative"},
        {"system", "control", "authoritative"},
    )
    _text(authority["system"], "authority.system", maximum=128)
    _text(authority["control"], "authority.control", maximum=128)
    if not isinstance(authority["authoritative"], bool):
        raise ValueError("authority.authoritative must be boolean")

    state = value["state"]
    if state not in SECURITY_STATES:
        raise ValueError("unsupported Wardveil security state")

    coverage = _mapping(value["coverage"], "coverage", {"status"}, {"status"})
    coverage_status = coverage["status"]
    if coverage_status not in COVERAGE_STATES:
        raise ValueError("unsupported Wardveil coverage status")

    evidence = _mapping(
        value["evidence"],
        "evidence",
        {"status", "observed_at", "valid_until", "references"},
        {"status", "observed_at", "references"},
    )
    evidence_status = evidence["status"]
    if evidence_status not in EVIDENCE_STATES:
        raise ValueError("unsupported Wardveil evidence status")
    observed_at = _timestamp(evidence["observed_at"], "evidence.observed_at")
    valid_until = None
    if "valid_until" in evidence:
        valid_until = _timestamp(evidence["valid_until"], "evidence.valid_until")
        if valid_until <= observed_at:
            raise ValueError("evidence.valid_until must be later than evidence.observed_at")
    _string_list(
        evidence["references"],
        "evidence.references",
        maximum_items=64,
        maximum_length=256,
    )

    claim = _mapping(
        value["claim"],
        "claim",
        {"protected_by_wardveil"},
        {"protected_by_wardveil"},
    )
    protected_claim = claim["protected_by_wardveil"]
    if not isinstance(protected_claim, bool):
        raise ValueError("claim.protected_by_wardveil must be boolean")

    explanation = _mapping(
        value["explanation"],
        "explanation",
        {"reason_codes", "legacy_presentation_state"},
        {"reason_codes", "legacy_presentation_state"},
    )
    _string_list(
        explanation["reason_codes"],
        "explanation.reason_codes",
        minimum_items=1,
        maximum_items=32,
        maximum_length=160,
    )
    if explanation["legacy_presentation_state"] not in LEGACY_PRESENTATION_STATES:
        raise ValueError("unsupported legacy presentation state")

    if coverage_status == "not_covered":
        if state != "not_covered" or protected_claim:
            raise ValueError("not_covered coverage must remain not_covered and unprotected")

    if state == "protected" or protected_claim:
        if state != "protected" or not protected_claim:
            raise ValueError("protected state and protected claim must agree")
        if authority["authoritative"] is not True:
            raise ValueError("protected evidence requires authoritative Wardveil evidence")
        if coverage_status != "covered":
            raise ValueError("protected evidence requires covered coverage")
        if evidence_status != "current" or valid_until is None:
            raise ValueError("protected evidence requires current evidence with valid_until")

        current_time = now or datetime.now(timezone.utc)
        if current_time.tzinfo is None or current_time.utcoffset() is None:
            raise ValueError("now must be timezone-aware")
        if observed_at > current_time:
            raise ValueError("future Wardveil evidence cannot establish protected state")
        if valid_until <= current_time:
            raise ValueError("expired Wardveil evidence cannot establish protected state")

    return deepcopy(dict(value))
