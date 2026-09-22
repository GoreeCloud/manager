"""Tests for bounded Wardveil Security State v2 source validation."""

from datetime import datetime, timezone

from django.test import SimpleTestCase

from integrations.wardveil import (
    WARDVEIL_CONTRACT_REPOSITORY,
    WARDVEIL_CONTRACT_REVISION,
    WARDVEIL_SECURITY_STATE_CONTRACT_ID,
    WARDVEIL_SECURITY_STATE_VERSION,
    validate_security_state,
)


class WardveilSecurityStateTests(SimpleTestCase):
    NOW = datetime(2026, 9, 22, 21, 0, tzinfo=timezone.utc)

    def _record(self, **overrides):
        value = {
            "contract_version": "0.2.0",
            "record_type": "security_state",
            "record_id": "manager-security-state-1",
            "scope": {"kind": "application", "id": "goreecloud-manager"},
            "authority": {
                "system": "wardveil-security",
                "control": "manager-security-state",
                "authoritative": True,
            },
            "state": "protected",
            "coverage": {"status": "covered"},
            "evidence": {
                "status": "current",
                "observed_at": "2026-09-22T20:30:00Z",
                "valid_until": "2026-09-22T21:30:00Z",
                "references": ["evidence+sha256:" + ("a" * 64) + ":manager/security-state"],
            },
            "claim": {"protected_by_wardveil": True},
            "explanation": {
                "reason_codes": ["current-authoritative-covered-evidence"],
                "legacy_presentation_state": "protected",
            },
        }
        value.update(overrides)
        return value

    def test_contract_provenance_is_pinned(self):
        self.assertEqual(WARDVEIL_CONTRACT_REPOSITORY, "GoreeCloud/wardveil")
        self.assertEqual(
            WARDVEIL_CONTRACT_REVISION,
            "9b41040ed48037451e660e860908316732384282",
        )
        self.assertEqual(
            WARDVEIL_SECURITY_STATE_CONTRACT_ID,
            "urn:goreecloud:wardveil:security-state:0.2.0",
        )
        self.assertEqual(WARDVEIL_SECURITY_STATE_VERSION, "0.2.0")

    def test_accepts_current_protected_record(self):
        validated = validate_security_state(self._record(), now=self.NOW)
        self.assertEqual(validated["state"], "protected")
        self.assertTrue(validated["claim"]["protected_by_wardveil"])

    def test_accepts_unknown_record_without_manufacturing_protection(self):
        record = self._record(
            authority={"system": "wardveil-security", "control": "manager-security-state", "authoritative": False},
            state="unknown",
            coverage={"status": "unknown"},
            evidence={
                "status": "unverified",
                "observed_at": "2026-09-22T20:30:00Z",
                "references": [],
            },
            claim={"protected_by_wardveil": False},
            explanation={"reason_codes": ["evidence-unverified"], "legacy_presentation_state": "unknown"},
        )
        validated = validate_security_state(record, now=self.NOW)
        self.assertEqual(validated["state"], "unknown")
        self.assertFalse(validated["claim"]["protected_by_wardveil"])

    def test_rejects_non_authoritative_protected_evidence(self):
        record = self._record(
            authority={"system": "wardveil-security", "control": "manager-security-state", "authoritative": False}
        )
        with self.assertRaises(ValueError):
            validate_security_state(record, now=self.NOW)

    def test_rejects_uncovered_or_noncurrent_protected_evidence(self):
        cases = (
            self._record(coverage={"status": "partial"}),
            self._record(evidence={
                "status": "stale",
                "observed_at": "2026-09-22T20:30:00Z",
                "valid_until": "2026-09-22T21:30:00Z",
                "references": [],
            }),
        )
        for record in cases:
            with self.subTest(record=record), self.assertRaises(ValueError):
                validate_security_state(record, now=self.NOW)

    def test_rejects_protected_record_without_valid_until(self):
        evidence = dict(self._record()["evidence"])
        evidence.pop("valid_until")
        with self.assertRaises(ValueError):
            validate_security_state(self._record(evidence=evidence), now=self.NOW)

    def test_rejects_expired_or_future_protected_evidence(self):
        expired = self._record(evidence={
            "status": "current",
            "observed_at": "2026-09-22T19:00:00Z",
            "valid_until": "2026-09-22T20:00:00Z",
            "references": [],
        })
        future = self._record(evidence={
            "status": "current",
            "observed_at": "2026-09-22T21:10:00Z",
            "valid_until": "2026-09-22T22:00:00Z",
            "references": [],
        })
        for record in (expired, future):
            with self.subTest(record=record), self.assertRaises(ValueError):
                validate_security_state(record, now=self.NOW)

    def test_rejects_invalid_validity_order(self):
        record = self._record(evidence={
            "status": "current",
            "observed_at": "2026-09-22T20:30:00Z",
            "valid_until": "2026-09-22T20:00:00Z",
            "references": [],
        })
        with self.assertRaises(ValueError):
            validate_security_state(record, now=self.NOW)

    def test_rejects_claim_and_state_disagreement(self):
        for record in (
            self._record(state="degraded"),
            self._record(claim={"protected_by_wardveil": False}),
        ):
            with self.subTest(record=record), self.assertRaises(ValueError):
                validate_security_state(record, now=self.NOW)

    def test_not_covered_must_remain_unprotected(self):
        invalid = self._record(coverage={"status": "not_covered"})
        with self.assertRaises(ValueError):
            validate_security_state(invalid, now=self.NOW)

        valid = self._record(
            state="not_covered",
            coverage={"status": "not_covered"},
            evidence={"status": "unverified", "observed_at": "2026-09-22T20:30:00Z", "references": []},
            claim={"protected_by_wardveil": False},
            explanation={"reason_codes": ["scope-not-covered"], "legacy_presentation_state": "unknown"},
        )
        self.assertEqual(validate_security_state(valid, now=self.NOW)["state"], "not_covered")

    def test_rejects_extra_missing_or_malformed_fields(self):
        extra = self._record(unexpected=True)
        missing = self._record()
        missing.pop("explanation")
        malformed = self._record(scope={"kind": "bogus", "id": "goreecloud-manager"})
        for record in (extra, missing, malformed):
            with self.subTest(record=record), self.assertRaises(ValueError):
                validate_security_state(record, now=self.NOW)

    def test_rejects_naive_timestamps_and_naive_now(self):
        record = self._record(evidence={
            "status": "current",
            "observed_at": "2026-09-22T20:30:00",
            "valid_until": "2026-09-22T21:30:00Z",
            "references": [],
        })
        with self.assertRaises(ValueError):
            validate_security_state(record, now=self.NOW)
        with self.assertRaises(ValueError):
            validate_security_state(self._record(), now=datetime(2026, 9, 22, 21, 0))

    def test_validation_returns_data_not_manager_security_authority(self):
        validated = validate_security_state(self._record(), now=self.NOW)
        self.assertIsInstance(validated, dict)
        self.assertFalse(hasattr(validated, "authorize"))
        self.assertFalse(hasattr(validated, "protect"))
        self.assertFalse(hasattr(validated, "execute"))
