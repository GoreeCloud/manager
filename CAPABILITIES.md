# GoreeCloud Manager — Capabilities

## Overview

GoreeCloud Manager currently provides a Development-stage administration and operational-visibility foundation. Capability claims below describe repository evidence and do not imply production acceptance.

## Core Capabilities

- Authenticated Django administration shell.
- Process-liveness and database-aware readiness endpoints.
- Server-rendered operational dashboards and integration views.
- Container packaging and automated repository validation.
- Supply-chain and source/image provenance validation foundations.

## Administrative Capabilities

- Read-only NetBird peer/private-network visibility.
- Read-only Healthchecks scheduled-job visibility.
- Read-only Uptime Kuma availability visibility.
- Delegated, sanitized Kopia status-artifact consumption.
- Delegated, sanitized Beszel resource-status consumption.
- Read-only GoreeCloud Tasks integration.
- Bounded Privacy Shield status presentation.
- Bounded Everkeep resilience-status presentation.
- Source-level Wardveil Security State v2 evidence validation.
- Source-level Mesh v1 coordination/governance evidence-envelope validation.
- Source-level GoreeCloud Policy v1 evaluation-request construction and decision-evidence validation.
- Source-level privacy-minimized GoreeCloud Observability v1 signal construction.

## Platform Integrations

### GoreeCloud Manager

This repository implements Manager itself. A separate Manager-to-Manager integration is not applicable.

### Privacy Shield

A sanitized read-only status boundary exists in source. Current-contract runtime and production acceptance remain pending.

### Wardveil Security

Manager now has a bounded source validator for the authoritative Wardveil Security State v2 contract pinned to the accepted Wardveil source revision. It validates security-state evidence shape, coverage/evidence/authority invariants, and protected-evidence timing without authenticating the producer or executing security controls. Live authenticated delivery, producer identity, evidence refresh, control execution, target-environment coverage validation, and production acceptance remain pending.

### Everkeep

A bounded resilience-status integration exists in source. Target-environment recovery evidence and current-contract production acceptance remain pending.

### Glaze UI

Current repository source is mapped to Glaze UI 1.6.0. This is source adoption only: rendered review, keyboard/200% text/accessibility acceptance, representative performance, rollback, deployed-equivalence, central consumer-registry acceptance, and production acceptance remain pending.

### GoreeCloud Mesh

Manager now has a source-validated consumer for current Mesh-authored coordination/governance evidence envelopes pinned to the corrected canonical Mesh source revision. It validates provenance, freshness, minimization, and authority-domain boundaries without reinterpreting producer outcomes. Live Mesh connectivity, discovery, Identity-backed authentication, evidence delivery/refresh, target-environment validation, and production acceptance remain pending.

### GoreeCloud Identity

Manager currently relies on its local Django authentication/session foundation. GoreeCloud Identity migration remains pending.

### GoreeCloud Policy

Manager now has source-validated helpers for the authoritative Policy v1 evaluation-request and decision contracts, pinned to the accepted Policy source revision. The source adapter constructs privacy-minimized request data, validates exact decision evidence and optional request/decision provenance, and deliberately provides no Policy transport or enforcement authority. Live authenticated decision exchange, distribution, freshness/expiry semantics, enforcement coordination, target-environment validation, and production acceptance remain pending.

### GoreeCloud Observability

Manager now has a source-validated, privacy-minimized producer adapter for the authoritative Observability v1 operational-signal contract, pinned to the accepted Observability source revision. It constructs contract-shaped evidence only; live authenticated publication, collection, freshness/completeness acceptance, retention, alerting, target-environment validation, and production acceptance remain pending.

GoreeCloud Sync remains separately governed and is not a tenth Integral Platform System.

## Data and Interoperability

Current integrations use bounded adapters, normalized fields, and sanitized artifacts where appropriate. Manager must not depend on undocumented private database layouts when a supported interface is required.

## Supported Platforms and Interfaces

The authoritative main manifest currently declares the web interface. Other clients or packaging experiments do not become supported production platforms without separate validation and lifecycle promotion.

## Security and Privacy Capabilities

- Authenticated administration foundation.
- Least-privilege/read-only integration preference.
- No direct Docker socket dependency for current approved integrations.
- Secret-minimization requirements.
- Sanitized health/status boundaries.
- Source and container supply-chain validation foundations.

## Resilience, Backup, and Recovery Capabilities

Manager declares backup, clean restore, export, and portability requirements for Manager-owned durable state. Target-environment recovery acceptance remains pending.

## Accessibility Capabilities

Current source includes keyboard focus, skip-link, reduced-motion, reduced-transparency, contrast, forced-colors, responsive-layout, and practical-target foundations. Current Stable Glaze UI 1.6.0 consumer acceptance remains pending.

## Automation and API Capabilities

Manager exposes health/readiness endpoints and integration-specific monitoring surfaces, can validate bounded Wardveil security-state evidence without turning it into authorization or security-control authority, can validate bounded Mesh-authored coordination/governance evidence without turning it into trust or mutation authority, can construct Policy v1 evaluation-request data and validate Policy decision evidence without enforcing it, and can construct Observability v1 operational-signal payloads from Manager-owned evidence. No live Wardveil, Mesh, Policy, or Observability transport is claimed. Automation must not convert producer evidence, Policy decision evidence, status evidence, or source-contract validation into unapproved operational mutation authority.

## Current Limitations

Manager remains Development and nonconformant. Production publication, production write authority, current Platform-System runtime acceptance, Glaze UI 1.6.0 consumer acceptance, deployment/rollback verification, release approval, and Stable qualification remain open.

## Capability Validation

Repository tests and CI can establish source/build/test evidence for exact revisions. They do not establish target-environment runtime, deployment, recovery, production, release, or Stable acceptance unless those gates are separately verified.
