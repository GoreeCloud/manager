from datetime import datetime, timedelta, timezone

import pytest

from integrations.mesh import (
    MESH_CONTRACT_REPOSITORY,
    MESH_CONTRACT_REVISION,
    MESH_EVIDENCE_ENVELOPE_CONTRACT,
    MESH_EVIDENCE_ENVELOPE_VERSION,
    validate_mesh_evidence_envelope,
)


def valid_envelope(now: datetime) -> dict:
    return {
        "version": MESH_EVIDENCE_ENVELOPE_VERSION,
        "id": "mesh-governance-001",
        "producer": {
            "system": "goreecloud-mesh",
            "repository": MESH_CONTRACT_REPOSITORY,
            "revision": MESH_CONTRACT_REVISION,
            "contract": MESH_EVIDENCE_ENVELOPE_CONTRACT,
        },
        "authority_domain": "governance",
        "subject": {
            "kind": "service",
            "id": "goreecloud-manager",
            "scope": "source-contract-adoption",
        },
        "assertion": "evidence-envelope-validation",
        "outcome": "validated",
        "source": "mesh://evidence/manager-source-contract",
        "observed_at": (now - timedelta(minutes=5)).isoformat(),
        "valid_until": (now + timedelta(minutes=55)).isoformat(),
        "data_class": "operational",
        "summary": "Bounded Mesh coordination evidence.",
        "payload_digest": "sha256:" + "a" * 64,
        "contains_user_content": False,
        "contains_secret_material": False,
    }


def test_accepts_current_mesh_envelope_without_reinterpreting_outcome():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)
    envelope = valid_envelope(now)
    envelope["outcome"] = "producer-defined-state"

    got = validate_mesh_evidence_envelope(envelope, evaluated_at=now)

    assert got["outcome"] == "producer-defined-state"
    assert got["producer"]["repository"] == "GoreeCloud/mesh"
    assert got["authority_domain"] == "governance"


def test_rejects_stale_precanonical_mesh_repository():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)
    envelope = valid_envelope(now)
    envelope["producer"]["repository"] = "GoreeCloud/goreecloud-mesh"

    with pytest.raises(ValueError, match="canonical GoreeCloud/mesh"):
        validate_mesh_evidence_envelope(envelope, evaluated_at=now)


def test_rejects_non_mesh_producer_in_bounded_adapter():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)
    envelope = valid_envelope(now)
    envelope["producer"]["system"] = "wardveil-security"

    with pytest.raises(ValueError, match="Mesh-authored evidence only"):
        validate_mesh_evidence_envelope(envelope, evaluated_at=now)


def test_rejects_authority_escalation():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)
    envelope = valid_envelope(now)
    envelope["authority_domain"] = "security"

    with pytest.raises(ValueError, match="coordination/governance"):
        validate_mesh_evidence_envelope(envelope, evaluated_at=now)


def test_rejects_expired_and_future_evidence():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)

    expired = valid_envelope(now)
    expired["observed_at"] = (now - timedelta(hours=2)).isoformat()
    expired["valid_until"] = (now - timedelta(hours=1)).isoformat()
    with pytest.raises(ValueError, match="expired"):
        validate_mesh_evidence_envelope(expired, evaluated_at=now)

    future = valid_envelope(now)
    future["observed_at"] = (now + timedelta(minutes=1)).isoformat()
    future["valid_until"] = (now + timedelta(hours=1)).isoformat()
    with pytest.raises(ValueError, match="after evaluation time"):
        validate_mesh_evidence_envelope(future, evaluated_at=now)


def test_rejects_privacy_unsafe_flags_and_bad_digest():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)

    for field in ("contains_user_content", "contains_secret_material"):
        envelope = valid_envelope(now)
        envelope[field] = True
        with pytest.raises(ValueError):
            validate_mesh_evidence_envelope(envelope, evaluated_at=now)

    envelope = valid_envelope(now)
    envelope["payload_digest"] = "sha256:not-a-digest"
    with pytest.raises(ValueError, match="payload_digest"):
        validate_mesh_evidence_envelope(envelope, evaluated_at=now)


def test_rejects_missing_or_extra_contract_fields():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)

    missing = valid_envelope(now)
    del missing["source"]
    with pytest.raises(ValueError, match="exact Mesh v1 fields"):
        validate_mesh_evidence_envelope(missing, evaluated_at=now)

    extra = valid_envelope(now)
    extra["trusted"] = True
    with pytest.raises(ValueError, match="exact Mesh v1 fields"):
        validate_mesh_evidence_envelope(extra, evaluated_at=now)


def test_rejects_non_mesh_contract_namespace_and_invalid_subject_shape():
    now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)

    wrong_contract = valid_envelope(now)
    wrong_contract["producer"]["contract"] = "contracts/identity.evidence.schema.json"
    with pytest.raises(ValueError, match="Mesh contract namespace"):
        validate_mesh_evidence_envelope(wrong_contract, evaluated_at=now)

    bad_subject = valid_envelope(now)
    bad_subject["subject"]["unexpected"] = "value"
    with pytest.raises(ValueError, match="subject must contain"):
        validate_mesh_evidence_envelope(bad_subject, evaluated_at=now)
