# GoreeCloud Policy Integration

## Status

**Development / source-contract adoption only.**

GoreeCloud Manager contains bounded source helpers for the authoritative GoreeCloud Policy v1 evaluation-request and decision contracts. This source integration does not establish a deployed Policy service, live decision exchange, policy distribution, enforcement, Manager authorization, or production acceptance.

## Authoritative contract provenance

- Repository: `GoreeCloud/policy`
- Authoritative source revision: `46071886da37a6566b69cc923005eef64cce2bcc`
- Request schema: `contracts/evaluation-request.schema.json`
- Request contract ID: `https://goreecloud.com/contracts/policy/evaluation-request/v1`
- Decision schema: `contracts/policy-decision.schema.json`
- Decision contract ID: `https://goreecloud.com/contracts/policy/decision/v1`

Manager pins that exact Policy source revision in `integrations/policy.py` so later Policy changes cannot silently alter the source contract represented by this increment.

## Implemented source boundary

`integrations/policy.py` provides two pure helpers:

- `build_evaluation_request(...)` constructs the exact Policy v1 request shape from explicit policy, authority, subject, resource, and action fields plus optional privacy-minimized context.
- `validate_policy_decision(...)` validates the exact Policy v1 decision field set, six-value decision vocabulary, string/list/boolean types, timezone-aware evaluation timestamp, and optional provenance binding back to the expected request.

The request helper rejects empty required fields, non-JSON-safe context values, and obvious secret-bearing context keys recursively. The decision validator fails closed on missing or extra fields, unsupported decisions, malformed arrays, non-boolean freshness, invalid timestamps, or mismatched policy/authority/subject/resource/action provenance.

The adapter is intentionally dependency-light. It performs no network request, authenticates to no external service, stores no policy decision, distributes no policy, mutates no Manager state, and introduces no reusable credential.

## Authority boundary

GoreeCloud Policy remains authoritative for shared policy representation, evaluation, decision coordination, distribution, explanation, provenance, and policy evidence. Manager remains authoritative only for Manager-owned facts and actions within separately accepted authorization and execution boundaries.

A structurally valid Policy decision with `decision: allow` is Policy decision evidence only. It is not, by itself, Manager authorization to execute an action. Manager execution authority must remain separately governed and accepted.

## Privacy and security boundary

Policy request context must be minimized to facts required for the evaluation. Passwords, authorization headers, API tokens, private keys, cookies, credentials, and other obvious secret-bearing context fields are rejected by the source helper. This source validation is a guardrail and does not replace Privacy Shield, Wardveil Security, or GoreeCloud Identity acceptance.

## Not yet implemented or accepted

This source increment does not establish:

- GoreeCloud Identity-backed Policy caller identity or service credentials;
- live authenticated HTTP or Mesh decision exchange;
- policy distribution, synchronization, or cache behavior;
- decision freshness/expiry behavior beyond validating the contract's `fresh` boolean and evaluation timestamp shape;
- Manager enforcement or mutation behavior based on Policy decisions;
- Policy obligations execution;
- Wardveil Security or Privacy Shield production acceptance of Policy-related behavior;
- target-environment connectivity, availability, monitoring, or rollback evidence;
- deployment, production approval, release promotion, or Stable qualification.

## Acceptance progression

Manager may advance Policy integration beyond `applicable-migration-required` only after the applicable caller identity, authenticated transport, runtime decision exchange, provenance/freshness semantics, distribution/enforcement boundaries, security/privacy acceptance, target-environment validation, recovery/rollback, production approval, release, and Stable gates are independently evidenced and accepted.
