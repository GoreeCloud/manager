# GoreeCloud Manager — Changelogs

**Status:** Authoritative repository changelog  
**Canonical repository:** `GoreeCloud/manager`  
**Lifecycle:** Development

## Purpose

This file records meaningful Manager implementation, governance, compatibility, and lifecycle changes. It is repository history, not a release announcement and not proof of deployment, production acceptance, or Stable qualification.

Google Drive changelog/roadmap copies are not authoritative under the GoreeCloud Repository Feature Tracking and Changelog Governance standard.

## 2026-09-22

### Policy v1 source contract adoption

- Added a pure Manager-side GoreeCloud Policy v1 evaluation-request builder and decision-evidence validator pinned to Policy source revision `46071886da37a6566b69cc923005eef64cce2bcc`.
- Added recursive context minimization, exact decision-field and vocabulary validation, timezone-aware evaluation timestamps, and optional request/decision provenance binding.
- Added focused tests and repository-local integration documentation.
- Changed Manager's Policy Platform Contract result from `applicable-blocked` to `applicable-migration-required` while preserving live caller identity, authenticated decision exchange, distribution, freshness/expiry, enforcement coordination, obligations handling, target-environment, and production gates.
- A validated Policy `allow` value remains decision evidence only and does not independently authorize Manager execution.

### Repository feature/changelog governance migration — PR #104

- Replaced the retired `FEATURE-ROADMAP.md` repository control with the mandatory `IMPLEMENTED-FEATURES.md`, `PLANNED-FEATURES.md`, and `CHANGELOGS.md` records.
- Migrated the meaningful obligations from both the repository roadmap and the former Drive-side Manager feature roadmap, including Glaze UI downstream acceptance, nine-system integration, Android signing/device acceptance, branch protection, production evidence, client lifecycle, planned MCP/tool gateway work, and production/Stable qualification.
- Updated repository-baseline validation so the three authoritative records are mandatory and the legacy roadmap is rejected if reintroduced.
- Exact candidate `9471818a813e71678080d607a750e6129f21f403` passed all seven applicable pull-request workflow families before merge; authoritative merge commit is `7431f521cb4c3448d10f35cfb2cb046e63139c69`.
- This governance migration changes feature/changelog authority and repository controls only; it does not advance production, release, or Stable status.

### Observability v1 source contract adoption — PR #102

- Added a privacy-minimized Manager-side GoreeCloud Observability v1 operational-signal constructor pinned to Observability source revision `a7f6a65f442d3e517baddbe7b6ce7c250d142c8c`.
- Added focused tests and repository-local integration documentation.
- Changed Manager's Observability Platform Contract result from `applicable-blocked` to `applicable-migration-required` while preserving live producer identity, authenticated publication/collection, freshness/completeness, retention, alerting, target-environment, and production gates.
- Exact PR head `f43113e1be4deb8579304e9fd20bd731242e0d4f` passed all eight applicable pull-request workflows before merge; authoritative merge commit is `0f8e78bd9f38cd3433b4dbed404371e909b4000a`.

## 2026-09-21

### Glaze UI 1.6.0 source adoption — PR #100

- Migrated the repository-local Manager presentation mapping to current Stable Glaze UI 1.6.0 source requirements.
- Kept rendered/browser, accessibility, representative-performance, rollback, deployed-equivalence, central consumer-registry, production, release, and Stable acceptance as separate downstream gates.
- Exact candidate `714a7e3680e6a1537a582806da3f669312abfa04` passed the eight applicable pull-request workflow families before merge; authoritative merge commit is `38d4e0e9bd0e36a5f1f231c1c4880a154e65474a`.

### Repository governance and Platform Contract 0.4 baseline — PR #99

- Added the governed repository-documentation baseline, `CAPABILITIES.md`, `.editorconfig`, pull-request template, fail-closed repository-baseline validator/regression coverage, and exact-revision Repository Baseline workflow.
- Corrected canonical repository/branding authority identifiers.
- Migrated Manager's source declaration to Platform Contract 0.4 with exactly nine Integral Platform Systems while keeping GoreeCloud Sync separately governed.
- Authoritative merge commit is `7a55c207c1c2c8df1955551bf9f80ef4f001e221`.

## Earlier development history

Earlier implementation history remains preserved in Git commit/PR history and repository documentation. This file was introduced when the repository adopted the mandatory GitHub-native changelog standard; entries above capture the meaningful stabilization and governance history verified during that migration rather than inventing unverified retrospective release claims.

## Maintenance rule

Update this file in the same governed workflow for meaningful implementation, compatibility, security/privacy boundary, migration, deprecation/removal, governance, release, or lifecycle changes. Record exact revisions/PRs where they materially improve traceability. Do not describe source or CI changes as deployed, production-accepted, released, or Stable unless those separate gates are actually verified.
