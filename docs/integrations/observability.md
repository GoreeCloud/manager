# GoreeCloud Observability Integration

## Status

**Development / source-contract adoption only.**

GoreeCloud Manager now contains a bounded producer adapter for the authoritative GoreeCloud Observability v1 operational-signal contract. This source integration does not establish a deployed Observability service, live signal publication, production monitoring coverage, or production acceptance.

## Authoritative contract provenance

- Repository: `GoreeCloud/observability`
- Authoritative source revision: `a7f6a65f442d3e517baddbe7b6ce7c250d142c8c`
- Contract schema: `contracts/operational-signal.schema.json`
- Contract ID: `https://goreecloud.com/contracts/observability/operational-signal/v1`

Manager pins that exact source revision in `integrations/observability.py` so a later Observability change cannot silently alter the producer contract represented by this source increment.

## Implemented source boundary

`integrations/observability.py` constructs privacy-minimized Manager-owned operational-signal payloads with:

- the exact Observability v1 state vocabulary;
- explicit component/source identity for `goreecloud-manager`;
- timezone-aware UTC observation and collection timestamps;
- bounded TTL values from 1 through 86400 seconds;
- optional correlation identifiers;
- optional collection-gap evidence;
- JSON-safe attributes with fail-closed rejection of obvious secret-bearing attribute names;
- explicit caller-selected state rather than inference that missing evidence means healthy.

The adapter is intentionally pure and dependency-light. It performs no network request, authenticates to no external service, stores no telemetry, and introduces no reusable credential.

## Authority and privacy boundary

GoreeCloud Observability remains authoritative for shared operational telemetry, health evidence, freshness, completeness, and correlation semantics. Manager remains authoritative only for the Manager-owned facts it produces.

Signals must contain operational evidence, not user content or reusable authentication material. Passwords, authorization headers, API tokens, private keys, cookies, credentials, and other obvious secret-bearing attributes are rejected by the source adapter. This validation is a guardrail, not a replacement for Privacy Shield or Wardveil Security acceptance.

Missing, stale, unavailable, or incomplete evidence must remain represented by the corresponding Observability state. A lack of evidence must never be converted to `healthy`.

## Not yet implemented or accepted

This source increment does not establish:

- GoreeCloud Identity-backed producer authentication;
- live HTTP or Mesh delivery to an Observability runtime;
- durable telemetry storage or accepted retention/deletion behavior;
- accepted collection coverage, freshness, or completeness;
- alerts, SLOs, incident automation, or diagnostic correlation;
- Privacy Shield or Wardveil production acceptance of telemetry behavior;
- Everkeep recovery/continuity acceptance for retained operational evidence;
- target-environment runtime validation;
- deployment, production approval, release promotion, or Stable qualification.

## Acceptance progression

Manager may advance Observability integration beyond `applicable-migration-required` only after the applicable live producer identity, authenticated transport, collector/runtime, privacy/security, freshness/completeness, retention/recovery, target-environment, and production gates are independently evidenced and accepted.
