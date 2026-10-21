# GoreeCloud Manager — Changelogs

**Status:** Authoritative repository changelog  
**Canonical repository:** `GoreeCloud/manager`  
**Lifecycle:** Development

## Purpose

This file records meaningful Manager implementation, governance, compatibility, and lifecycle changes. It is repository history, not a release announcement and not proof of deployment, production acceptance, or Stable qualification.

Google Drive changelog/roadmap copies are not authoritative under the GoreeCloud Repository Feature Tracking and Changelog Governance standard.

## 2026-10-21

### Native Linux desktop Glaze Overview and critical CA trust repair — PR #113

- Refined read-only Linux desktop status hierarchy, one-surface Overview scrolling, Light/Dark semantic warnings, accessible refresh, and non-decorative navigation.
- Updated locked server-side `certifi` to patched `2026.10.19` with a PyPI-verified wheel checksum after the October emSign CA compromise; preserved strict, fail-closed OSV vulnerability scanning.
- PR #113 was merged as commit `021f5e5cc96324ffdf0ab563f947b04e41394b5e` after eight green workflow families. The native Linux workstation installation was verified at v0.2.9 with an actual read-only SSH connection, light/dark visual testing, and preserved private configuration; no production server deployment was performed.

### Active Docker health accuracy — v0.2.10 merged source and verified Linux installation

- Separate live health monitoring from the historical last-known health of exited containers. Manager no longer calls old, stopped rollback containers active unhealthy workloads.
- Keep historical health visible as `Last: …` inside the full Docker inventory; omit historical stale health from the Needs attention filter.
- Add synthetic parser regression coverage and retain the operational state of all containers for inspection.
- The v0.2.10 source advanced to `main` as commit `d6f9ccf9014102ecc1455019fd75eb4bf2cd10fb` and was subsequently refined by PR #117. The authoritative post-PR #117 revision is `f1a97eaa785da245f69ff061c98b02e9333c12dd`.
- v0.2.10 was installed on the connected Linux laptop on October 21, 2026 using the staged installer after a verified compressed backup of v0.2.9; the installed application reconnected by read-only SSH and showed Docker AVAILABLE without the previous stale unhealthy alerts. This is laptop verification, not a server deployment or Stable release.

### Native Glaze controls and live Docker health filters — PR #117

- Reconciled v0.2.10 health filters against active running containers; exited container historical status remains visible under Stopped/All and within details without creating false current-health alarms.
- Improved Qt Light/Dark settings dropdowns and keyboard-usable numeric fields; increased inventory row spacing, label room, and accessible selection contrast. Bundled required chevron assets into native Linux Debian acceptance packaging.
- Prevented premature all-clear messages while system or infrastructure checks are incomplete.
- PR #117 merged as commit `f1a97eaa785da245f69ff061c98b02e9333c12dd` after all eight workflow families passed; 24 desktop/configuration/Docker regression tests passed from the exact merged checkout on the connected laptop.
- Post-install Linux readback verified v0.2.10, installed assets and desktop entry, private configuration permissions, working read-only SSH, Docker inventory, NetBird information, and rendered Overview/Containers/Network. Three failed systemd units and three connecting NetBird peers remain unresolved operational findings tracked by [issue #114](https://github.com/GoreeCloud/manager/issues/114).
- No production VPS changes or production/Stable qualification are claimed.

## 2026-09-22

### Wardveil Security State v2 source adoption

- Added a bounded Manager-side validator for the authoritative Wardveil Security State v2 contract pinned to Wardveil source revision `9b41040ed48037451e660e860908316732384282`.
- Validates exact state/coverage/evidence/scope vocabularies, nested field boundaries, bounded identifiers/references, timezone-aware evidence validity, and Wardveil's protected/not-covered conditional invariants.
- Fails closed when a protected claim is non-authoritative, uncovered, non-current, future-dated, missing an expiry, or expired; valid source data remains evidence only and does not grant Manager authorization or security-control authority.
- Moves Manager's Wardveil Platform Contract source state from blocked to migration-required while preserving authenticated producer identity/delivery, evidence refresh, security-control execution, target-environment coverage, production, release, and Stable gates.

### Mesh evidence-envelope v1 source adoption

- Added a bounded Manager-side validator for current Mesh-authored coordination/governance evidence envelopes pinned to corrected Mesh source revision `6bd0678faf94cbadcaaac7f2c31aa72ecca1b372`.
- Validates canonical `GoreeCloud/mesh` producer provenance, exact envelope fields, authority boundaries, subject shape, timestamp ordering/freshness, data class, minimization flags, and optional SHA-256 payload digest while preserving producer-defined outcomes.
- Restricts this increment to Mesh-authored evidence; evidence from Identity, Wardveil Security, Privacy Shield, Everkeep, and Glaze UI remains subject to separately verified producer contracts.
- Moves Manager's Mesh Platform Contract source state from blocked to migration-required while preserving live connectivity, discovery, Identity-backed authentication, evidence delivery/refresh, target-environment, production, release, and Stable gates.

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
