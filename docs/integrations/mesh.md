# GoreeCloud Mesh Integration

## Status

**Development / source-contract adoption only.**

GoreeCloud Manager contains a bounded consumer validator for current Mesh-authored coordination/governance evidence envelopes. This does not establish a live Manager-to-Mesh connection, service discovery, runtime evidence collection, trust promotion, or production acceptance.

## Authoritative contract provenance

- Repository: `GoreeCloud/mesh`
- Authoritative source revision: `6bd0678faf94cbadcaaac7f2c31aa72ecca1b372`
- Contract schema: `contracts/mesh.evidence-envelope.schema.json`
- Contract ID: `https://goreecloud.org/contracts/mesh.evidence-envelope.schema.json`
- Envelope version: `goreecloud.evidence-envelope.v1`
- Mesh producer system: `goreecloud-mesh`
- Canonical Mesh producer repository: `GoreeCloud/mesh`

The pinned revision includes the canonical-provenance correction merged through Mesh PR #49. Manager intentionally does not accept the stale pre-canonical producer repository `GoreeCloud/goreecloud-mesh`.

## Implemented source boundary

`integrations/mesh.py` validates Mesh-authored envelopes with:

- exact top-level v1 fields plus only the documented optional summary/digest fields;
- exact Mesh producer identity and canonical repository provenance;
- exact lowercase 40-character producer revision formatting;
- Mesh-owned `contracts/mesh.*` contract namespace;
- Mesh authority domains limited to `coordination` and `governance`;
- bounded subject, assertion, outcome, and source fields;
- timezone-aware observation and validity timestamps;
- fail-closed future/expired evidence handling when current evidence is required;
- the contract data classes `public`, `operational`, and `derived`;
- explicit rejection unless `contains_user_content` and `contains_secret_material` are both `false`;
- optional lowercase SHA-256 payload-digest validation.

The producer-defined `outcome` is preserved as opaque Mesh-domain evidence. Manager does not reinterpret it into security, privacy, identity, Policy, recovery, or execution authority.

## Deliberate scope restriction

This adapter accepts **Mesh-authored** evidence only. It does not validate evidence authored by GoreeCloud Identity, Wardveil Security, Privacy Shield, Everkeep, or Glaze UI. Those producers retain their own authority and require separately verified current producer contracts before Manager may consume their evidence.

## Not yet implemented or accepted

This source increment does not establish:

- a network connection to a Mesh runtime;
- service discovery or reachability integration;
- GoreeCloud Identity-backed Mesh authentication;
- evidence refresh, polling, subscription, or durable Manager-side storage;
- producer delivery verification in a target environment;
- cross-system trust promotion or decision authority;
- runtime connectivity/reachability acceptance;
- deployment, production approval, release promotion, or Stable qualification.

Manager's Platform Contract result therefore remains `applicable-migration-required` after this source adoption rather than conformant or accepted.
