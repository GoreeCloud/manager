import unittest
from datetime import datetime, timedelta, timezone

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


class MeshEvidenceEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 22, 20, 50, tzinfo=timezone.utc)

    def test_accepts_current_mesh_envelope_without_reinterpreting_outcome(self):
        envelope = valid_envelope(self.now)
        envelope["outcome"] = "producer-defined-state"

        got = validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

        self.assertEqual(got["outcome"], "producer-defined-state")
        self.assertEqual(got["producer"]["repository"], "GoreeCloud/mesh")
        self.assertEqual(got["authority_domain"], "governance")

    def test_rejects_stale_precanonical_mesh_repository(self):
        envelope = valid_envelope(self.now)
        envelope["producer"]["repository"] = "GoreeCloud/goreecloud-mesh"

        with self.assertRaisesRegex(ValueError, "canonical GoreeCloud/mesh"):
            validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

    def test_rejects_non_mesh_producer_in_bounded_adapter(self):
        envelope = valid_envelope(self.now)
        envelope["producer"]["system"] = "wardveil-security"

        with self.assertRaisesRegex(ValueError, "Mesh-authored evidence only"):
            validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

    def test_rejects_authority_escalation(self):
        envelope = valid_envelope(self.now)
        envelope["authority_domain"] = "security"

        with self.assertRaisesRegex(ValueError, "coordination/governance"):
            validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

    def test_rejects_expired_and_future_evidence(self):
        expired = valid_envelope(self.now)
        expired["observed_at"] = (self.now - timedelta(hours=2)).isoformat()
        expired["valid_until"] = (self.now - timedelta(hours=1)).isoformat()
        with self.assertRaisesRegex(ValueError, "expired"):
            validate_mesh_evidence_envelope(expired, evaluated_at=self.now)

        future = valid_envelope(self.now)
        future["observed_at"] = (self.now + timedelta(minutes=1)).isoformat()
        future["valid_until"] = (self.now + timedelta(hours=1)).isoformat()
        with self.assertRaisesRegex(ValueError, "after evaluation time"):
            validate_mesh_evidence_envelope(future, evaluated_at=self.now)

    def test_rejects_privacy_unsafe_flags_and_bad_digest(self):
        for field in ("contains_user_content", "contains_secret_material"):
            with self.subTest(field=field):
                envelope = valid_envelope(self.now)
                envelope[field] = True
                with self.assertRaises(ValueError):
                    validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

        envelope = valid_envelope(self.now)
        envelope["payload_digest"] = "sha256:not-a-digest"
        with self.assertRaisesRegex(ValueError, "payload_digest"):
            validate_mesh_evidence_envelope(envelope, evaluated_at=self.now)

    def test_rejects_missing_or_extra_contract_fields(self):
        missing = valid_envelope(self.now)
        del missing["source"]
        with self.assertRaisesRegex(ValueError, "exact Mesh v1 fields"):
            validate_mesh_evidence_envelope(missing, evaluated_at=self.now)

        extra = valid_envelope(self.now)
        extra["trusted"] = True
        with self.assertRaisesRegex(ValueError, "exact Mesh v1 fields"):
            validate_mesh_evidence_envelope(extra, evaluated_at=self.now)

    def test_rejects_non_mesh_contract_namespace_and_invalid_subject_shape(self):
        wrong_contract = valid_envelope(self.now)
        wrong_contract["producer"]["contract"] = "contracts/identity.evidence.schema.json"
        with self.assertRaisesRegex(ValueError, "Mesh contract namespace"):
            validate_mesh_evidence_envelope(wrong_contract, evaluated_at=self.now)

        bad_subject = valid_envelope(self.now)
        bad_subject["subject"]["unexpected"] = "value"
        with self.assertRaisesRegex(ValueError, "subject must contain"):
            validate_mesh_evidence_envelope(bad_subject, evaluated_at=self.now)


if __name__ == "__main__":
    unittest.main()
