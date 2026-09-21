# GoreeCloud Manager — GLAZE UI V1.6 Source Adoption

## Status and authority

**Lifecycle:** Development source adoption  
**Consumer target:** GLAZE UI V1.6 / 1.6.0 Stable  
**Canonical Glaze repository:** `GoreeCloud/glaze-ui`  
**Accepted release source:** `a7180679ea851389e0f3004515f9a25f420e716d`  
**Stable runtime entrypoint:** `js/glaze-v1.6.0.mjs`  
**Known-good shared rollback baseline:** 1.5.1  
**Manager consumer acceptance:** pending  
**Manager production acceptance:** not established

This document defines the repository-local presentation contract for GoreeCloud Manager. The current Manager source maps its authenticated application shell and operational surfaces to the current Stable GLAZE UI V1.6 presentation language while preserving Manager's read-only security model and the authority of every integrated system.

This is **source adoption**, not downstream consumer acceptance. Passing repository tests cannot grant Glaze consumer-registry acceptance, deployment approval, production acceptance, release approval, or Manager Stable qualification.

## Authority boundary

GLAZE UI is presentation-only. It may present state supplied by Manager or by an authoritative integration, but it must not manufacture privacy, security, recovery, identity, policy, observability, connectivity, authorization, deployment, or production truth.

Manager remains responsible for application behavior and least-privilege integration boundaries. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, GoreeCloud Policy, and GoreeCloud Observability retain their own authority.

A favorable color, material, status chip, loading state, or animation can never upgrade an unavailable, stale, blocked, unknown, or unverified operational state.

## Repository-local mapping

Manager does not copy the canonical Glaze runtime wholesale into the Django application. The repository implements a bounded product-specific CSS/HTML/JavaScript mapping for the V1.6 presentation behavior actually exercised by the authenticated interface.

- `core/templates/core/base.html` declares the V1.6 source target, shared landmarks, GoreeCloud identity, local assets, Soft Glaze navigation chrome, adaptive action grouping, and the application main target.
- `core/static/core/css/app.css` owns Manager-specific product layout, operational surfaces, status presentation, product color roles, and responsive content composition.
- `core/static/core/css/glaze-ui.css` owns the repository-local V1.6 cross-cutting contract: 48 px interactive minimums, optional 56 px Touch Assistance, Soft Glaze navigation material, solid operational surfaces, focus, form behavior, safe-area resilience, performance material reduction, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, and unsupported-backdrop fallbacks.
- `core/static/core/js/theme.js` owns the browser-local System/Light/Dark preference and maps explicit choices to the V1.6 `data-glz-appearance` semantic without transmitting the setting.
- `tests/test_glaze_ui_contract.py` fails closed when the source mapping, privacy boundary, local-only dependency rule, or required V1.6 fallback behavior drifts.

The local CSS is not represented as a byte-identical copy of `js/glaze-v1.6.0.mjs`. The canonical Glaze release remains the design-system authority; Manager's repository-local mapping remains application-specific evidence.

## Material and hierarchy

Manager is an operational administration console, so expressive treatment is intentionally bounded.

Persistent navigation chrome may use V1.6 **Soft Glaze**. Primary operational reading surfaces—hero regions, cards, metrics, recovery panels, authentication content, and status details—remain solid or raised surfaces. Glass is not a universal card treatment.

Manager does not add visual richness merely to demonstrate design-system capabilities. Optional V1.6 systems are exercised only when they serve a real application need.

## Interaction sizing and input behavior

The V1.6 source mapping uses a 48 px minimum interactive target. An explicit `data-glz-touch-assistance="true"` presentation context raises the effective minimum to 56 px without changing logical or keyboard order.

Native input, select, textarea, and button semantics are preserved. Manager does not replace native controls with role-mimicking elements merely for visual styling.

Focus remains visible and semantic. Keyboard navigation order follows DOM order, and adaptive action grouping must not reorder actions in a way that changes meaning or accessibility.

## Appearance and first paint

Manager supports System, Light, and Dark appearance modes.

The local appearance script runs before stylesheets so an explicit browser-local preference can be applied before first stylesheet-driven paint. Explicit Light or Dark choices set both the existing Manager theme attribute and the V1.6 `data-glz-appearance` semantic. System mode removes explicit appearance overrides and follows the operating-system preference.

The preference is stored only in browser `localStorage` under `goreecloud-manager-theme`. It is not written to the Manager database, sent to an integration, used for analytics, or used for profiling.

Manager does not infer performance or accessibility settings from undocumented device heuristics such as processor count or memory size.

## Accessibility and resilience

The shared shell and product surfaces must preserve:

- semantic header, navigation, main, form, status, and alert relationships;
- a keyboard-accessible skip link and focusable main target;
- persistent form labels and native input semantics;
- visible focus indicators;
- text that remains meaningful without relying on color alone;
- 200% text and narrow-screen reflow without clipping essential state;
- Reduced Motion behavior that removes nonessential transition/spatial motion;
- Reduced Transparency behavior that removes backdrop dependence;
- Increased Contrast behavior that strengthens boundaries and text cues;
- Forced Colors / High Contrast operation using system colors;
- solid raised fallbacks when backdrop filtering is unavailable;
- safe-area aware layout and horizontally resilient navigation;
- local-only presentation dependencies.

## Performance adaptation

V1.6 performance presentation is explicit rather than inferred.

`data-glaze-performance="constrained"` reduces the effective navigation blur. `data-glaze-performance="minimal"` removes blur and increases material opacity. These attributes change presentation only; they never hide required operational information or change integration state.

The application does not automatically assign a performance state from hardware heuristics in this source slice.

## Privacy and browser dependency boundary

The Manager browser presentation remains self-contained. The authenticated application must not require remote fonts, remote scripts, remote stylesheets, analytics, advertising, telemetry SDKs, externally hosted icons, or other presentation resources that would add unnecessary third-party browser requests.

Local presentation state must not become tracking state.

## Truthful operational status

Manager may display provider state only within the authority and freshness of the owning integration.

V1.6 status presentation must preserve explicit text labels for configuration, healthy, degraded, misconfigured, unavailable, planned, disabled, recovery, privacy, and work-management states. Styling may reinforce those states but cannot replace them.

Missing or failed integration evidence must continue to fail soft for the Manager shell and fail closed for stronger claims.

## Source validation

Repository CI validates the exact pull-request head and includes:

```bash
node --check core/static/core/js/theme.js
python manage.py collectstatic --noinput
python manage.py check
python manage.py test
```

The Glaze source tests verify the V1.6 declaration, Soft Glaze boundary, solid operational surfaces, 48/56 px sizing, local appearance mapping, accessibility and performance fallbacks, local-only dependencies, static product identity, native form behavior, and shared-shell inheritance.

Successful source validation establishes only repository-local source/build evidence.

## Consumer acceptance boundary

Current shared Glaze authority requires fresh repository-local 1.6.0 consumer evidence. The central consumer registry currently records GoreeCloud Manager as **adoption-required** and production-ineligible. That registry also retains a historical Manager repository identifier; this Manager repository does not silently rewrite that separate authority.

Before Manager can claim current Glaze consumer acceptance, the applicable process must verify the exact Manager revision through representative authenticated rendering, keyboard review, 200% text, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, applicable assistive technology, representative performance/fallback behavior, deterministic build/provenance, rollback, deployed-byte equivalence where applicable, and central consumer-registry reconciliation.

## Release and production boundary

GLAZE UI V1.6 being Stable does not make Manager Stable.

This source adoption does not establish:

- deployed Manager UI equivalence;
- production publication;
- production runtime acceptance;
- central consumer-registry acceptance;
- representative human visual acceptance;
- assistive-technology acceptance;
- application-specific performance acceptance;
- rollback acceptance;
- Manager release approval; or
- Manager Stable qualification.

Those gates remain separate and fail closed.
