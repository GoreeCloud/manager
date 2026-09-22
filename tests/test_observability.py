"""Tests for the source-level GoreeCloud Observability v1 producer contract."""

from datetime import UTC, datetime

from django.test import SimpleTestCase

from integrations.observability import (
    OBSERVABILITY_CONTRACT_ID,
    OBSERVABILITY_CONTRACT_REVISION,
    OBSERVABILITY_STATES,
    build_operational_signal,
)


OBSERVED_AT = datetime(2026, 9, 22, 19, 0, tzinfo=UTC)


class ObservabilitySignalTests(SimpleTestCase):
    def test_contract_provenance_is_pinned(self):
        self.assertEqual(
            OBSERVABILITY_CONTRACT_ID,
            "https://goreecloud.com/contracts/observability/operational-signal/v1",
        )
        self.assertEqual(
            OBSERVABILITY_CONTRACT_REVISION,
            "a7f6a65f442d3e517baddbe7b6ce7c250d142c8c",
        )

    def test_builds_required_manager_signal_fields(self):
        payload = build_operational_signal(
            signal_id="manager-liveness-1",
            signal_type="process-liveness",
            state="healthy",
            observed_at=OBSERVED_AT,
            ttl_seconds=30,
            correlation_id="request-123",
            attributes={"scope": "process"},
        )

        self.assertEqual(
            payload,
            {
                "signal_id": "manager-liveness-1",
                "component_id": "goreecloud-manager",
                "source": "goreecloud-manager",
                "signal_type": "process-liveness",
                "state": "healthy",
                "observed_at": "2026-09-22T19:00:00Z",
                "collected_at": "2026-09-22T19:00:00Z",
                "ttl_seconds": 30,
                "correlation_id": "request-123",
                "attributes": {"scope": "process"},
            },
        )

    def test_all_authoritative_states_are_accepted(self):
        expected = {
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
        self.assertEqual(OBSERVABILITY_STATES, expected)

        for state in expected:
            with self.subTest(state=state):
                payload = build_operational_signal(
                    signal_id=f"state-{state}",
                    signal_type="contract-test",
                    state=state,
                    observed_at=OBSERVED_AT,
                )
                self.assertEqual(payload["state"], state)

    def test_unknown_state_preserves_collection_gap(self):
        payload = build_operational_signal(
            signal_id="manager-readiness-unknown",
            signal_type="readiness",
            state="unknown",
            observed_at=OBSERVED_AT,
            collection_gaps=("readiness evidence unavailable",),
        )

        self.assertEqual(payload["state"], "unknown")
        self.assertEqual(
            payload["collection_gaps"], ["readiness evidence unavailable"]
        )

    def test_rejects_unsupported_state(self):
        with self.assertRaises(ValueError):
            build_operational_signal(
                signal_id="invalid-state",
                signal_type="contract-test",
                state="ok",
                observed_at=OBSERVED_AT,
            )

    def test_rejects_invalid_ttl(self):
        for ttl in (0, 86401, True, 1.5):
            with self.subTest(ttl=ttl), self.assertRaises(ValueError):
                build_operational_signal(
                    signal_id="invalid-ttl",
                    signal_type="contract-test",
                    state="unknown",
                    observed_at=OBSERVED_AT,
                    ttl_seconds=ttl,
                )

    def test_rejects_naive_timestamps(self):
        with self.assertRaises(ValueError):
            build_operational_signal(
                signal_id="naive-time",
                signal_type="contract-test",
                state="unknown",
                observed_at=datetime(2026, 9, 22, 19, 0),
            )

    def test_rejects_sensitive_attribute_names_recursively(self):
        cases = (
            {"api_token": "test-value"},
            {"nested": {"Authorization": "test-value"}},
            {"private-key": "test-value"},
        )
        for attributes in cases:
            with self.subTest(attributes=attributes), self.assertRaises(ValueError):
                build_operational_signal(
                    signal_id="sensitive-attribute",
                    signal_type="contract-test",
                    state="unknown",
                    observed_at=OBSERVED_AT,
                    attributes=attributes,
                )

    def test_rejects_non_finite_or_non_json_attribute_values(self):
        cases = ({"load": float("nan")}, {"value": object()})
        for attributes in cases:
            with self.subTest(attributes=attributes), self.assertRaises(ValueError):
                build_operational_signal(
                    signal_id="invalid-attribute",
                    signal_type="contract-test",
                    state="unknown",
                    observed_at=OBSERVED_AT,
                    attributes=attributes,
                )
