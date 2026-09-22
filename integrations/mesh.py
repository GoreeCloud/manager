"""Bounded GoreeCloud Mesh evidence-envelope v1 validation helpers.

This module validates current Mesh-authored coordination/governance evidence from
the authoritative GoreeCloud Mesh contract. It performs no network request,
discovers no service, authenticates no producer, refreshes no evidence, and does
not convert a valid envelope into Manager trust or mutation authority.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

MESH_CONTRACT_REPOSITORY = "GoreeCloud/mesh"
MESH_CONTRACT_REVISION = "6bd0678faf94cbadcaaac7f2c31aa72ecca1b372"
MESH_EVIDENCE_ENVELOPE_CONTRACT = "contracts/mesh.evidence-envelope.schema.json"
MESH_EVIDENCE_ENVELOPE_CONTRACT_ID = (
    "https://goreecloud.org/contracts/mesh.evidence-envelope.schema.json"
)
MESH_EVIDENCE_ENVELOPE_VERSION = "goreecloud.evidence-envelope.v1"
MESH_PRODUCER_SYSTEM = "goreecloud-mesh"
MESH_AUTHORITY_DOMAINS = frozenset({"coordination", "governance"})
MESH_DATA_CLASSES = frozenset({"public", "operational", "derived"})

_REQUIRED_FIELDS = frozenset(
    {
        "version",
        "id",
        "producer",
        "authority_domain",
        "subject",
        "assertion",
        "outcome",
        "source",
        "observed_at",
        "valid_until",
        "data_class",
        "contains_user_content",
        "contains_secret_material",
    }
)
_OPTIONAL_FIELDS = frozenset({"summary", "payload_digest"})
_PRODUCER_FIELDS = frozenset({"system", "repository", "revision", "contract"})
_SUBJECT_REQUIRED_FIELDS = frozenset({"kind", "id"})
_SUBJECT_OPTIONAL_FIELDS = frozenset({"scope"})
_REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def _nonempty_string(value: object, *, field: str, max_length: int | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if max_length is not None and len(normalized) > max_length:
        raise ValueError(f"{field} must be at most {max_length} characters")
    return normalized


def _timestamp(value: object, *, field: str) -> tuple[str, datetime]:
    text = _nonempty_string(value, field=field)
    parse_value = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(parse_value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone offset")
    return text, parsed.astimezone(timezone.utc)


def validate_mesh_evidence_envelope(
    envelope: Mapping[str, Any],
    *,
    evaluated_at: datetime | None = None,
    require_current: bool = True,
) -> dict[str, Any]:
    """Validate a current Mesh-authored evidence envelope without reinterpreting it."""

    if not isinstance(envelope, Mapping):
        raise ValueError("envelope must be an object")

    keys = set(envelope)
    allowed = _REQUIRED_FIELDS | _OPTIONAL_FIELDS
    missing = sorted(_REQUIRED_FIELDS - keys)
    extra = sorted(keys - allowed)
    if missing or extra:
        raise ValueError(
            f"envelope must contain the exact Mesh v1 fields; missing={missing}, extra={extra}"
        )

    if envelope["version"] != MESH_EVIDENCE_ENVELOPE_VERSION:
        raise ValueError("unsupported Mesh evidence-envelope version")

    evidence_id = _nonempty_string(envelope["id"], field="id", max_length=128)

    producer = envelope["producer"]
    if not isinstance(producer, Mapping) or set(producer) != _PRODUCER_FIELDS:
        raise ValueError("producer must contain the exact Mesh v1 producer fields")
    if producer["system"] != MESH_PRODUCER_SYSTEM:
        raise ValueError("this bounded Manager adapter accepts Mesh-authored evidence only")
    if producer["repository"] != MESH_CONTRACT_REPOSITORY:
        raise ValueError("Mesh producer repository does not match canonical GoreeCloud/mesh")
    revision = _nonempty_string(producer["revision"], field="producer.revision")
    if not _REVISION_PATTERN.fullmatch(revision):
        raise ValueError("producer.revision must be an exact lowercase 40-character Git revision")
    contract = _nonempty_string(producer["contract"], field="producer.contract")
    if not contract.startswith("contracts/mesh."):
        raise ValueError("producer.contract must belong to the Mesh contract namespace")

    authority_domain = _nonempty_string(envelope["authority_domain"], field="authority_domain")
    if authority_domain not in MESH_AUTHORITY_DOMAINS:
        raise ValueError("Mesh evidence cannot assert authority outside coordination/governance")

    subject = envelope["subject"]
    if not isinstance(subject, Mapping):
        raise ValueError("subject must be an object")
    subject_keys = set(subject)
    allowed_subject = _SUBJECT_REQUIRED_FIELDS | _SUBJECT_OPTIONAL_FIELDS
    if _SUBJECT_REQUIRED_FIELDS - subject_keys or subject_keys - allowed_subject:
        raise ValueError("subject must contain kind/id and optional scope only")
    normalized_subject = {
        "kind": _nonempty_string(subject["kind"], field="subject.kind", max_length=64),
        "id": _nonempty_string(subject["id"], field="subject.id", max_length=256),
    }
    if "scope" in subject:
        scope = subject["scope"]
        if not isinstance(scope, str) or len(scope.strip()) > 256:
            raise ValueError("subject.scope must be a string of at most 256 characters")
        normalized_subject["scope"] = scope.strip()

    assertion = _nonempty_string(envelope["assertion"], field="assertion", max_length=128)
    outcome = _nonempty_string(envelope["outcome"], field="outcome", max_length=128)
    source = _nonempty_string(envelope["source"], field="source", max_length=512)

    observed_text, observed_at = _timestamp(envelope["observed_at"], field="observed_at")
    valid_text, valid_until = _timestamp(envelope["valid_until"], field="valid_until")
    if valid_until <= observed_at:
        raise ValueError("valid_until must be after observed_at")

    now = evaluated_at or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("evaluated_at must be timezone-aware")
    now = now.astimezone(timezone.utc)
    if observed_at > now:
        raise ValueError("observed_at cannot be after evaluation time")
    if require_current and now > valid_until:
        raise ValueError("Mesh evidence envelope is expired")

    data_class = _nonempty_string(envelope["data_class"], field="data_class")
    if data_class not in MESH_DATA_CLASSES:
        raise ValueError("invalid Mesh evidence data_class")

    if envelope["contains_user_content"] is not False:
        raise ValueError("Mesh evidence envelope must declare contains_user_content=false")
    if envelope["contains_secret_material"] is not False:
        raise ValueError("Mesh evidence envelope must declare contains_secret_material=false")

    normalized: dict[str, Any] = {
        "version": MESH_EVIDENCE_ENVELOPE_VERSION,
        "id": evidence_id,
        "producer": {
            "system": MESH_PRODUCER_SYSTEM,
            "repository": MESH_CONTRACT_REPOSITORY,
            "revision": revision,
            "contract": contract,
        },
        "authority_domain": authority_domain,
        "subject": normalized_subject,
        "assertion": assertion,
        "outcome": outcome,
        "source": source,
        "observed_at": observed_text,
        "valid_until": valid_text,
        "data_class": data_class,
        "contains_user_content": False,
        "contains_secret_material": False,
    }

    if "summary" in envelope:
        summary = envelope["summary"]
        if not isinstance(summary, str) or len(summary.strip()) > 512:
            raise ValueError("summary must be a string of at most 512 characters")
        normalized["summary"] = summary.strip()

    if "payload_digest" in envelope:
        digest = _nonempty_string(envelope["payload_digest"], field="payload_digest")
        if not _DIGEST_PATTERN.fullmatch(digest):
            raise ValueError("payload_digest must use sha256:<64 lowercase hex characters>")
        normalized["payload_digest"] = digest

    return normalized
