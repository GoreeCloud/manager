# GoreeCloud Manager — Privacy Policy

## Scope

GoreeCloud Manager is an administrative and operational presentation surface. It must minimize the private information it receives, stores, logs, and displays.

The repository is in Development. Source contracts and tests do not by themselves establish production data-processing practice.

## Privacy authority

GoreeCloud Privacy Shield remains authoritative for shared privacy controls and privacy-state decisions. Manager must consume or present privacy evidence without creating broader privacy authority.

## Data minimization

Manager integrations should return only the fields required for the approved administrative purpose. Ordinary status payloads, logs, dashboards, exports, tests, and documentation must not contain reusable credentials, private keys, recovery material, unnecessary personal content, raw private messages, unrestricted browsing/activity data, or unrelated private diagnostics.

Where a bounded status, digest, reference, count, or redacted summary is sufficient, Manager should not ingest the underlying private payload.

## Credentials and browser state

Reusable integration credentials belong in protected runtime configuration rather than source control or ordinary Manager records. Appearance preference may remain browser-local where implemented and must not be repurposed for profiling or analytics.

## Integrated systems

Manager must preserve the privacy boundaries of Privacy Shield, Wardveil Security, Everkeep, Identity, Mesh, Policy, Observability, and application-specific producers. A read-only integration does not authorize broader collection or disclosure.

## Failure behavior

Missing, stale, malformed, unauthorized, or unaccepted privacy-sensitive evidence must not silently become a healthy or approved state. Failure messaging should be useful without exposing private payloads.

This policy must be reconciled when verified implementation or accepted production behavior materially changes.
