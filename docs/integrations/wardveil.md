# GoreeCloud Wardveil Security Integration

## Status

**Development / source-contract adoption only.**

GoreeCloud Manager contains a bounded, read-only validator for Wardveil Security State v2 evidence. This source integration does not establish live Wardveil connectivity, authenticate a Wardveil producer, execute a security control, authorize a Manager action, or establish production protection.

## Authoritative contract provenance

- Repository: `GoreeCloud/wardveil`
- Authoritative source revision: `9b41040ed48037451e660e860908316732384282`
- Contract schema: `contracts/wardveil.security-state.v2.schema.json`
- Contract ID: `urn:goreecloud:wardveil:security-state:0.2.0`
- Contract version: `0.2.0`

Manager pins that exact source revision in `integrations/wardveil.py` so later Wardveil changes cannot silently alter the source contract represented by this increment.

## Implemented source boundary

`integrations/wardveil.py` validates Wardveil-authored security-state records with:

- the exact Security State v2 top-level shape and nested object boundaries;
- exact security-state, coverage-state, evidence-state, scope-kind, and legacy-presentation vocabularies;
- bounded canonical identifiers, controls, reason codes, and evidence references;
- timezone-aware observation and validity timestamps;
- validity ordering consistent with Wardveil's reference model;
- fail-closed handling for protected claims whose evidence is non-authoritative, uncovered, non-current, future-dated, missing an expiry, or already expired;
- the contract invariant that `not_covered` coverage remains `not_covered` and cannot carry a Wardveil protection claim.

The validator returns detached data only. It has no network transport, no reusable credential, no protection method, no policy-execution bridge, no quarantine/response function, and no Manager mutation authority.

## Authority and provenance boundary

Wardveil Security remains authoritative for GoreeCloud security and trust decisions. Manager only validates the shape and bounded semantics of a record it has been given.

A structurally valid record does **not** prove that its sender is Wardveil. Authenticated producer identity, protected transport, live evidence delivery/refresh, and target-environment verification remain separate acceptance gates.

Likewise, a valid `protected` record is evidence data. Manager must not convert source-contract validation into independent authorization, protection coverage, or execution authority.

## Not yet implemented or accepted

This source increment does not establish:

- GoreeCloud Identity-backed Wardveil service authentication;
- live HTTP, Mesh, event, polling, or subscription delivery from Wardveil;
- authenticated producer provenance for individual records;
- accepted evidence refresh or durable Manager-side security-state storage;
- security-control execution, quarantine, response, containment, or remediation authority;
- independent Manager authorization from Wardveil state;
- accepted production protection coverage or current target-system coverage;
- target-environment validation, deployment, production approval, release promotion, or Stable qualification.

## Acceptance progression

Manager may advance Wardveil integration beyond `applicable-migration-required` only after the applicable authenticated producer identity, protected delivery, freshness/coverage, target-environment, security-control boundary, production, release, and lifecycle gates are independently evidenced and accepted.
