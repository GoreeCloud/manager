# GoreeCloud Manager — User Manual

## Current audience

GoreeCloud Manager is in Development. This manual describes the current source-level administration experience for developers and authorized administrators. It is not a statement that Manager is production published or Stable.

## Starting Manager for development

Use the repository setup instructions in `README.md` to create the Python environment, configure a development-only secret, apply migrations, create an administrator account, and start the Django server.

## Health endpoints

- `/healthz/` reports process liveness only.
- `/readyz/` includes database-aware readiness.
- Integration-specific health endpoints are sanitized monitoring signals and are not substitutes for the authoritative state of the integrated system.

## Integrations

Manager uses read-only APIs or sanitized delegated artifacts wherever practical. An integration card or status row does not grant Manager authority over the producer. If an integration is unavailable, stale, malformed, or unaccepted, treat the displayed limitation as real rather than assuming a healthy state.

## Appearance and accessibility

The current interface provides System, Light, and Dark appearance behavior together with keyboard focus, reduced-motion, reduced-transparency, contrast, and forced-colors foundations. The implemented source mapping is Glaze UI 1.3.0; migration and acceptance against current Stable Glaze UI 1.6.0 remain required.

## Safety

Do not place reusable passwords, tokens, private keys, recovery codes, production configuration, private content, or unrestricted diagnostic payloads in ordinary Manager documentation or status artifacts.

Do not interpret a passing repository workflow as production authorization, deployment approval, recovery proof, or Stable qualification.

## More information

See `README.md`, `SECURITY.md`, `PRIVACY POLICY.md`, `CAPABILITIES.md`, and `FEATURE-ROADMAP.md`.
