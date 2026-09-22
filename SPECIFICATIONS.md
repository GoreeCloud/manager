# GoreeCloud Manager — Specifications

## Status

**Lifecycle:** Development  
**Canonical repository:** `GoreeCloud/manager`  
**Platform Contract:** 0.4  
**Implemented Glaze UI source mapping:** 1.6.0  
**Required current Stable Glaze UI target:** 1.6.0  
**Production acceptance:** not established  
**Stable qualification:** not established

## Role

GoreeCloud Manager is the native administration and operational console for GoreeCloud. It provides bounded visibility and, only where separately authorized and accepted, administrative control over GoreeCloud systems without taking over the authority of the systems it presents.

## Current implemented foundation

The current main-line implementation provides an authenticated Django web application, process-liveness and database-aware readiness endpoints, read-only operational integrations, sanitized delegated-artifact integrations, a read-only GoreeCloud Tasks adapter, repository CI, container packaging, a repository-local Glaze UI 1.6.0 source presentation mapping with consumer acceptance still pending, a source-level Wardveil Security State v2 evidence validator, a source-level Mesh v1 coordination/governance evidence-envelope validator, a source-level GoreeCloud Policy v1 evaluation-request/decision-evidence adapter, and a source-level GoreeCloud Observability v1 operational-signal constructor.

Current source includes bounded Privacy Shield and Everkeep status integrations, a Wardveil Security State v2 source validator that does not authenticate producers or execute security controls, a Mesh v1 source consumer restricted to Mesh-authored coordination/governance evidence, a Policy v1 source-contract adapter that does not call or enforce Policy, and a privacy-minimized Observability v1 producer-contract adapter. GoreeCloud Identity remains blocked pending accepted migration/runtime evidence. Wardveil live authenticated delivery/control execution/coverage acceptance, Mesh live connectivity/authentication/evidence delivery, Policy live authenticated decision exchange/distribution/freshness/enforcement behavior, and Observability live publication/collection/freshness/completeness/retention remain migration-required.

## Authority boundaries

- Manager presents and coordinates; it does not manufacture authoritative security, privacy, recovery, identity, policy, observability, or connectivity truth.
- Privacy Shield owns privacy decisions and privacy-state authority.
- Wardveil Security owns security and trust decisions. A structurally valid Wardveil security-state record remains Wardveil evidence and does not independently authorize Manager action or establish authenticated producer provenance.
- Everkeep owns continuity and recovery assurance.
- GoreeCloud Identity owns identity, authentication, authorization, and service credentials.
- GoreeCloud Mesh owns private connectivity and bounded platform coordination. A structurally valid Mesh evidence envelope remains producer evidence and does not independently establish Manager trust or execution authority.
- GoreeCloud Policy owns shared policy representation and decision coordination. A validated Policy `allow` value is decision evidence only and does not independently authorize Manager execution.
- GoreeCloud Observability owns shared operational telemetry and evidence correlation.
- Glaze UI owns shared presentation and interaction requirements.
- GoreeCloud Sync remains separately governed and is not a tenth Integral Platform System.

## Current blockers

Manager has not completed Platform Contract 0.4 runtime acceptance, Glaze UI 1.6.0 downstream consumer acceptance, representative rendered/accessibility/performance/rollback acceptance, live Identity/Mesh/Policy/Observability integration, live authenticated Wardveil delivery and security-control/coverage acceptance, target-environment backup/restore qualification, deployment and rollback verification, production publication, release approval, or Stable qualification.
