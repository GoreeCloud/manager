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

The current main-line implementation provides an authenticated Django web application, process-liveness and database-aware readiness endpoints, read-only operational integrations, sanitized delegated-artifact integrations, a read-only GoreeCloud Tasks adapter, repository CI, container packaging, a repository-local Glaze UI 1.6.0 source presentation mapping with consumer acceptance still pending, and a source-level GoreeCloud Observability v1 operational-signal constructor.

Current source includes bounded Privacy Shield and Everkeep status integrations plus a privacy-minimized Observability v1 producer-contract adapter. Wardveil Security, GoreeCloud Mesh, GoreeCloud Identity, and GoreeCloud Policy remain blocked or migration-required until accepted contracts and runtime evidence exist. Observability live publication, collection, freshness/completeness acceptance, retention, and production evidence remain migration-required.

## Authority boundaries

- Manager presents and coordinates; it does not manufacture authoritative security, privacy, recovery, identity, policy, observability, or connectivity truth.
- Privacy Shield owns privacy decisions and privacy-state authority.
- Wardveil Security owns security and trust decisions.
- Everkeep owns continuity and recovery assurance.
- GoreeCloud Identity owns identity, authentication, authorization, and service credentials.
- GoreeCloud Mesh owns private connectivity and bounded platform coordination.
- GoreeCloud Policy owns shared policy representation and decision coordination.
- GoreeCloud Observability owns shared operational telemetry and evidence correlation.
- Glaze UI owns shared presentation and interaction requirements.
- GoreeCloud Sync remains separately governed and is not a tenth Integral Platform System.

## Current blockers

Manager has not completed Platform Contract 0.4 runtime acceptance, Glaze UI 1.6.0 downstream consumer acceptance, representative rendered/accessibility/performance/rollback acceptance, live Identity/Mesh/Policy/Observability integration, Wardveil runtime acceptance, target-environment backup/restore qualification, deployment and rollback verification, production publication, release approval, or Stable qualification.
