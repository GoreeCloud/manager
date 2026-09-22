# GoreeCloud Manager — Planned Features

**Status:** Authoritative repository planned-feature record  
**As of:** 2026-09-22  
**Canonical repository:** `GoreeCloud/manager`  
**Lifecycle:** Development

## Purpose

This file records planned, incomplete, migration-required, and acceptance-gated Manager work. It preserves the meaningful obligations from the retired repository `FEATURE-ROADMAP.md` and the former Drive-side `GoreeCloud/Feature Roadmap/GoreeCloud Manager/FEATURE-ROADMAP.docx` without retaining Google Drive as a feature authority.

Actionable implementation work remains governed through GoreeCloud Tasks Management and repository issues/PRs as applicable. A planned feature is not implemented merely because it appears here.

## Planned and incomplete work

| ID | Planned feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| PF-001 | Complete whole-application Glaze UI 1.6.0 consumer acceptance: authenticated rendered/browser review, keyboard navigation, 200% text, reduced-motion/transparency, increased-contrast/forced-colors, applicable assistive technology, adaptive/form-factor behavior, interaction states, representative performance, Human Visual Excellence, rollback, deployed-equivalence, central consumer-registry reconciliation, release, and production evidence. | P0 | Source mapping is implemented; downstream acceptance remains open. |
| PF-002 | Complete all architecturally applicable nine-system integrations while preserving each owning system's authority, least privilege, data minimization, provenance/freshness checks, and fail-closed behavior. Keep GoreeCloud Sync separately governed. | P0 | Platform Contract 0.4 source declaration is implemented. Privacy Shield and Everkeep have bounded source foundations; Observability has a v1 source producer adapter; Identity, Mesh, Wardveil runtime acceptance, Policy, live Observability, applicable Sync visibility, and target-environment acceptance remain incomplete. |
| PF-003 | Establish protected Android production signing and physical-device acceptance for the exact validated release package, including approved external signing identity, protected signing environment, public certificate fingerprint, exact unsigned/signed hashes, signature verification, installation/behavior validation, representative Glaze UI review, and explicit Android lifecycle classification. | P0 | Pending approval-controlled execution; issue #66 remains open. No production signing identity/private signing material/signed accepted APK/physical-device production acceptance is established. |
| PF-004 | Protect authoritative `main` with enforced repository rules requiring reviewed pull requests and permanent Manager readiness checks, preventing force pushes and branch deletion, preserving the approved merge strategy, and independently verifying bypass behavior. | P0 | Governance blocker; issue #47 remains open. Live GitHub readback on 2026-09-22 reports `main` as unprotected with no required checks. |
| PF-005 | Complete the production-readiness evidence manifest against the exact target environment with non-secret evidence references, timestamps, and verifier identity for publication, runtime, monitoring, notification, backup/restore, rollback, platform integrations, credentials, network paths, and all other governed categories. | P0 | Pending/incomplete. Disposable/source CI is not target-environment acceptance. |
| PF-006 | Maintain and complete client-platform lifecycle acceptance for Linux desktop, Android, responsive/browser behavior, secure navigation, rollback, package provenance, and platform-specific release evidence without conflating package/source validation with product Stable status. | P1 | Incremental. Android remains gated by PF-003; additional platform/release acceptance remains open. |
| PF-007 | Implement the planned provider-neutral Manager MCP / approved tool gateway only after read-only integrations and production-readiness controls are mature. Begin with read-only structured resources and narrow tools, explicit authentication/authorization, audit, sanitization, kill switches, no reusable-secret disclosure, and no raw shell/socket/database authority. | P1 | Planned only. No general Manager MCP production authority is established. Write-capable tools require separate per-tool governance and acceptance. |
| PF-008 | Complete Manager production and Stable qualification with exact-revision runtime validation, accepted platform integrations, current Glaze acceptance, live repository governance, recovery/rollback proof, monitoring/alerting, secure release provenance/signing, representative-target validation, explicit production approval, and lifecycle evidence. | P0 | Pending. Manager remains Development; source validation and green CI do not establish Release Candidate, production, release, or Stable status. |
| PF-009 | Complete live GoreeCloud Identity integration where shared identity/service credentials are required. | P0 | Not accepted. Manager currently relies on local Django authentication/session foundations. |
| PF-010 | Complete accepted GoreeCloud Mesh integration for authorized platform visibility/coordination against the current nine-system producer contract. | P0 | Not accepted. Historical Manager Mesh work must not become current authority until reconciled with current producer contracts. |
| PF-011 | Complete accepted Wardveil Security administration/status integration with privacy-minimized evidence and current canonical producer identity. | P0 | Not accepted. Historical consumer work remains subject to producer-contract reconciliation. |
| PF-012 | Complete GoreeCloud Policy decision/evidence integration, including current contract adoption, live authenticated decision exchange where applicable, provenance/freshness validation, enforcement-coordination boundaries, and production acceptance without transferring Policy authority to Manager. | P0 | Source contract adoption is the next bounded stabilization increment; live runtime/enforcement/production acceptance remains open. |
| PF-013 | Complete live GoreeCloud Observability publication/collection, producer identity/authentication, freshness/completeness acceptance, retention/deletion behavior, diagnostics/alerting, recovery, target-environment validation, and production acceptance. | P0 | v1 source signal construction is implemented; live runtime acceptance remains migration-required. |
| PF-014 | Complete separately governed GoreeCloud Sync visibility/administration integration where architecturally applicable. | P1 | Open; Sync is not a tenth Integral Platform System. |

## Governance controls migrated from the legacy roadmap

Feature state changes require authoritative evidence. Actionable unfinished work must be represented in GoreeCloud Tasks Management when required. Repository feature records, implementation evidence, issues/PRs, and applicable lifecycle records must remain reconciled; Google Drive roadmap copies are no longer an authoritative synchronization target.

## Maintenance rule

Update this file in the same governed repository workflow whenever planned scope, priority, dependency, lifecycle disposition, or implementation state materially changes. When a planned feature becomes implemented, move its implemented truth to `IMPLEMENTED-FEATURES.md` while retaining any still-open acceptance obligations here rather than falsely marking the whole capability complete.
