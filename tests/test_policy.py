"""Tests for the source-level GoreeCloud Policy v1 contracts."""

from django.test import SimpleTestCase

from integrations.policy import (
    POLICY_CONTRACT_REVISION,
    POLICY_DECISION_CONTRACT_ID,
    POLICY_DECISIONS,
    POLICY_EVALUATION_REQUEST_CONTRACT_ID,
    build_evaluation_request,
    validate_policy_decision,
)


class PolicyContractTests(SimpleTestCase):
    def _request(self):
        return build_evaluation_request(
            policy_id="manager-admin-action",
            policy_version="1",
            authority="goreecloud-policy",
            subject="manager-operator",
            resource="goreecloud-manager/settings",
            action="view",
            context={"request_source": "manager"},
        )

    def _decision(self, **overrides):
        value = {
            "decision": "allow",
            "policy_id": "manager-admin-action",
            "policy_version": "1",
            "authority": "goreecloud-policy",
            "subject": "manager-operator",
            "resource": "goreecloud-manager/settings",
            "action": "view",
            "reason": "matched read-only operator rule",
            "matched_rule_ids": ["read-only-operator"],
            "obligations": [],
            "evaluated_at": "2026-09-22T20:00:00Z",
            "fresh": True,
        }
        value.update(overrides)
        return value

    def test_contract_provenance_is_pinned(self):
        self.assertEqual(
            POLICY_CONTRACT_REVISION,
            "46071886da37a6566b69cc923005eef64cce2bcc",
        )
        self.assertEqual(
            POLICY_EVALUATION_REQUEST_CONTRACT_ID,
            "https://goreecloud.com/contracts/policy/evaluation-request/v1",
        )
        self.assertEqual(
            POLICY_DECISION_CONTRACT_ID,
            "https://goreecloud.com/contracts/policy/decision/v1",
        )

    def test_builds_exact_request_shape(self):
        payload = self._request()
        self.assertEqual(
            payload,
            {
                "policy_id": "manager-admin-action",
                "policy_version": "1",
                "authority": "goreecloud-policy",
                "subject": "manager-operator",
                "resource": "goreecloud-manager/settings",
                "action": "view",
                "context": {"request_source": "manager"},
            },
        )

    def test_rejects_empty_required_request_fields(self):
        fields = (
            "policy_id",
            "policy_version",
            "authority",
            "subject",
            "resource",
            "action",
        )
        base = {
            "policy_id": "p",
            "policy_version": "1",
            "authority": "a",
            "subject": "s",
            "resource": "r",
            "action": "view",
        }
        for field in fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                build_evaluation_request(**{**base, field: " "})

    def test_rejects_sensitive_context_recursively(self):
        cases = (
            {"api_token": "test-value"},
            {"nested": {"Authorization": "test-value"}},
            {"private-key": "test-value"},
        )
        for context in cases:
            with self.subTest(context=context), self.assertRaises(ValueError):
                build_evaluation_request(
                    policy_id="p",
                    policy_version="1",
                    authority="a",
                    subject="s",
                    resource="r",
                    action="view",
                    context=context,
                )

    def test_rejects_non_json_context_values(self):
        with self.assertRaises(ValueError):
            build_evaluation_request(
                policy_id="p",
                policy_version="1",
                authority="a",
                subject="s",
                resource="r",
                action="view",
                context={"object": object()},
            )

    def test_authoritative_decision_vocabulary_is_exact(self):
        self.assertEqual(
            POLICY_DECISIONS,
            {"allow", "deny", "conditional", "defer", "indeterminate", "error"},
        )
        for value in POLICY_DECISIONS:
            with self.subTest(value=value):
                validated = validate_policy_decision(self._decision(decision=value))
                self.assertEqual(validated["decision"], value)

    def test_rejects_extra_or_missing_decision_fields(self):
        extra = self._decision(unexpected="value")
        with self.assertRaises(ValueError):
            validate_policy_decision(extra)

        missing = self._decision()
        missing.pop("reason")
        with self.assertRaises(ValueError):
            validate_policy_decision(missing)

    def test_rejects_malformed_arrays_and_freshness(self):
        cases = (
            self._decision(matched_rule_ids="rule"),
            self._decision(obligations=[1]),
            self._decision(fresh=1),
        )
        for decision in cases:
            with self.subTest(decision=decision), self.assertRaises(ValueError):
                validate_policy_decision(decision)

    def test_rejects_invalid_or_naive_evaluation_timestamp(self):
        for value in ("not-a-time", "2026-09-22T20:00:00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_policy_decision(self._decision(evaluated_at=value))

    def test_rejects_provenance_mismatch_against_expected_request(self):
        request = self._request()
        fields = (
            "policy_id",
            "policy_version",
            "authority",
            "subject",
            "resource",
            "action",
        )
        for field in fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_policy_decision(
                    self._decision(**{field: "different"}),
                    expected_request=request,
                )

    def test_valid_allow_remains_data_not_manager_execution_authority(self):
        validated = validate_policy_decision(
            self._decision(),
            expected_request=self._request(),
        )
        self.assertEqual(validated["decision"], "allow")
        self.assertFalse(hasattr(validated, "execute"))
        self.assertFalse(hasattr(validated, "authorize"))
