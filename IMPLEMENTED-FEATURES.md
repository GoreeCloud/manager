# GoreeCloud Manager — Implemented Features

**Status:** Authoritative repository feature record  
**As of:** 2026-09-22  
**Canonical repository:** `GoreeCloud/manager`  
**Lifecycle:** Development

## Purpose

This file records Manager features and source capabilities that are supported by current repository evidence. It does not convert source implementation, CI success, packaging, or documentation into deployment, production acceptance, release approval, or Stable qualification.

Google Drive feature-roadmap copies are retired as feature authority under the GoreeCloud Repository Feature Tracking and Changelog Governance standard. GitHub repository records are authoritative for feature state.

## Implemented source capabilities

| ID | Implemented feature / capability | Evidence and boundary |
| --- | --- | --- |
| IF-001 | Authenticated Django administration foundation with process-liveness and database-aware readiness endpoints. | `README.md`, `SPECIFICATIONS.md`, `core/`, `/healthz/`, `/readyz/`. Development/source capability only. |
| IF-002 | Read-only operational integration foundations for NetBird, Healthchecks, Uptime Kuma, GoreeCloud Tasks, delegated Kopia status, delegated Beszel status, Privacy Shield status, and Everkeep resilience status. | `integrations/`, `core/`, integration documentation, tests. Individual live/current-contract and production acceptance remains separately gated. |
| IF-003 | Repository governance baseline with mandatory documentation, pull-request template, exact-revision Repository Baseline workflow, and fail-closed baseline validation/regression tests. | `scripts/validate_repository_baseline.py`, `scripts/test_repository_baseline.py`, `.github/workflows/repository-baseline.yml`. Live branch protection is not established by these source controls. |
| IF-004 | Platform Contract 0.4 source declaration evaluating exactly nine Integral Platform Systems while keeping GoreeCloud Sync separately governed. | `goreecloud.platform.yaml`; source declaration is integrated, while applicable runtime/platform-system acceptance remains independently gated. |
| IF-005 | Repository-local Glaze UI 1.6.0 source mapping for the Manager interface. | `docs/glaze-ui.md`, `core/static/core/css/glaze-ui.css`, `CAPABILITIES.md`; merged through PR #100 as source adoption. Rendered/accessibility/performance/rollback/deployed-equivalence/consumer-registry/production acceptance remains open. |
| IF-006 | Privacy-minimized GoreeCloud Observability v1 operational-signal construction for Manager-owned evidence. | `integrations/observability.py`, `tests/test_observability.py`, `docs/integrations/observability.md`; merged through PR #102. No live authenticated publication, collection, retention, alerting, target-environment, or production acceptance is claimed. |
| IF-007 | Container packaging, supply-chain evidence generation, exact build/provenance validation, and permanent readiness workflow foundations. | `Dockerfile`, `compose.yml`, `scripts/`, `.github/workflows/`. These are source/CI controls, not production acceptance. |
| IF-008 | Client packaging foundations for Linux desktop and Android, including debug/unsigned Android release tooling and externally controlled signing handoff/verification foundations. | `desktop-client/`, `android-client/`, `packaging/`; production Android signing and physical-device release acceptance remain open. |
| IF-009 | GoreeCloud Policy v1 evaluation-request construction and decision-evidence validation with exact contract provenance, secret-minimized context, timezone-aware decision timestamps, and optional request/decision provenance binding. | `integrations/policy.py`, `tests/test_policy.py`, `docs/integrations/policy.md`. No Policy runtime call, distribution, enforcement, Manager mutation authority, target-environment, or production acceptance is claimed; a validated `allow` remains decision evidence only. |
| IF-010 | GoreeCloud Mesh evidence-envelope v1 validation for current Mesh-authored coordination/governance evidence with canonical repository provenance, freshness, minimization, subject, authority-domain, and digest checks. | `integrations/mesh.py`, `tests/test_mesh.py`, `docs/integrations/mesh.md`; pinned to corrected Mesh revision `6bd0678faf94cbadcaaac7f2c31aa72ecca1b372`. No live Mesh connectivity, authentication, evidence delivery/refresh, target-environment, or production acceptance is claimed. |
| IF-011 | Wardveil Security State v2 evidence validation with exact contract provenance, bounded state/coverage/evidence semantics, timezone-aware validity checks, and fail-closed protected-claim invariants. | `integrations/wardveil.py`, `tests/test_wardveil.py`, `docs/integrations/wardveil.md`; pinned to Wardveil revision `9b41040ed48037451e660e860908316732384282`. No live authenticated Wardveil delivery, producer authentication, security-control execution, protection-coverage acceptance, target-environment, or production acceptance is claimed. |

## Authority boundary

Manager presents and coordinates accepted provider state; it does not manufacture Identity, security, privacy, recovery, Mesh, Policy, Observability, or Glaze UI authority. An implemented adapter or a successful workflow is evidence only for the exact source/build/test scope it validates.

## Maintenance rule

Update this file in the same governed repository workflow whenever a feature becomes implemented, materially changes, is removed, or has its evidence/boundary changed. Do not add a feature solely because it is planned, documented, or represented by an unmerged branch.
