"""Source-level contract tests for GoreeCloud Manager's Glaze UI V1.6 mapping."""

from __future__ import annotations

import re
from pathlib import Path

from django.test import SimpleTestCase

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BASE_TEMPLATE = REPOSITORY_ROOT / "core/templates/core/base.html"
APP_CSS = REPOSITORY_ROOT / "core/static/core/css/app.css"
GLAZE_CSS = REPOSITORY_ROOT / "core/static/core/css/glaze-ui.css"
THEME_JS = REPOSITORY_ROOT / "core/static/core/js/theme.js"
MANAGER_MARK = REPOSITORY_ROOT / "core/static/core/img/manager-mark.svg"
GLAZE_DOC = REPOSITORY_ROOT / "docs/glaze-ui.md"
PRIMARY_TEMPLATES = (
    REPOSITORY_ROOT / "core/templates/core/login.html",
    REPOSITORY_ROOT / "core/templates/core/overview.html",
    REPOSITORY_ROOT / "core/templates/core/tasks.html",
    REPOSITORY_ROOT / "core/templates/core/everkeep.html",
    REPOSITORY_ROOT / "core/templates/core/privacy_shield.html",
)


class GlazeUiContractTests(SimpleTestCase):
    """Keep Manager's bounded V1.6 source mapping truthful and reviewable."""

    @staticmethod
    def _read(path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_shared_shell_declares_private_goreecloud_v16_identity(self):
        base = self._read(BASE_TEMPLATE)

        self.assertIn('<html lang="en" data-glaze-version="1.6">', base)
        self.assertIn('data-glaze-ui="manager"', base)
        self.assertIn('data-glaze-version="1.6.0"', base)
        self.assertIn('data-glaze-surface="glaze"', base)
        self.assertIn('data-glaze-material-level="soft-glaze"', base)
        self.assertIn('data-glaze-action-group="adaptive"', base)
        self.assertIn('data-glaze-reachability="compact"', base)
        self.assertIn("glaze-navigation-capsule", base)
        self.assertIn("viewport-fit=cover", base)
        self.assertIn('content="noindex, nofollow, noarchive"', base)
        self.assertIn('name="referrer" content="same-origin"', base)
        self.assertIn("core/img/manager-mark.svg", base)
        self.assertIn("core/css/app.css", base)
        self.assertIn("core/css/glaze-ui.css", base)
        self.assertIn('href="#main-content"', base)
        self.assertIn('id="main-content" tabindex="-1"', base)

    def test_v16_semantics_are_explicit_and_product_mapped(self):
        css = self._read(GLAZE_CSS)

        for contract in (
            '--glaze-contract-version: "1.6.0"',
            "--glaze-canvas: var(--bg)",
            "--glaze-surface: var(--surface)",
            "--glaze-surface-strong: var(--surface-strong)",
            "--glaze-accent: var(--accent)",
            "--glaze-success: var(--good)",
            "--glaze-warning: var(--warning)",
            "--glaze-danger: var(--danger)",
            "--glaze-focus-ring: var(--accent)",
            "--glaze-selection: var(--accent-surface)",
            "--glaze-touch-min: 3rem",
            "--glaze-touch-assistance-min: 3.5rem",
            "--glaze-effective-touch-min: var(--glaze-touch-min)",
            "--glaze-target-min: var(--glaze-effective-touch-min)",
            "--glaze-shape-standard: 1rem",
            "--glaze-shape-hero: 2rem",
            "--glaze-effective-blur: var(--glaze-glass-functional-blur)",
            "--glaze-effective-opacity: .88",
            "--glaze-motion-scale: 1",
            'data-glz-touch-assistance="true"',
            'data-glaze-performance="constrained"',
            'data-glaze-performance="minimal"',
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, css)

        self.assertIn('site-header[data-glaze-material-level="soft-glaze"]', css)
        self.assertIn("background: var(--glaze-surface-strong)", css)
        self.assertIn("border-radius: var(--glaze-shape-hero)", css)
        self.assertIn("glaze-navigation-capsule", css)

    def test_v16_preserves_native_forms_and_truthful_status_presentation(self):
        css = self._read(GLAZE_CSS)
        login = self._read(REPOSITORY_ROOT / "core/templates/core/login.html")
        overview = self._read(REPOSITORY_ROOT / "core/templates/core/overview.html")

        self.assertIn('input:not([type="hidden"])', css)
        self.assertIn("select", css)
        self.assertIn("textarea", css)
        self.assertIn("Username {{ form.username }}", login)
        self.assertIn("Password {{ form.password }}", login)
        self.assertIn('role="alert"', login)
        self.assertNotIn('role="switch"', login)
        self.assertIn("{{ integration.state }}", overview)
        self.assertIn("status-{{ integration.state }}", overview)

    def test_documentation_binds_v16_source_without_claiming_acceptance(self):
        doc = self._read(GLAZE_DOC)

        for contract in (
            "GLAZE UI V1.6",
            "1.6.0",
            "a7180679ea851389e0f3004515f9a25f420e716d",
            "js/glaze-v1.6.0.mjs",
            "1.5.1",
            "source adoption",
            "consumer acceptance",
            "presentation-only",
            "production acceptance",
            "consumer registry",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, doc)

    def test_explicit_appearance_is_applied_before_stylesheets(self):
        base = self._read(BASE_TEMPLATE)
        theme_script = base.index("core/js/theme.js")
        app_stylesheet = base.index("core/css/app.css")
        glaze_stylesheet = base.index("core/css/glaze-ui.css")

        self.assertLess(theme_script, app_stylesheet)
        self.assertLess(theme_script, glaze_stylesheet)
        self.assertNotRegex(base, r'<script[^>]*\bdefer\b[^>]*core/js/theme\.js')

        theme = self._read(THEME_JS)
        self.assertIn('const storageKey = "goreecloud-manager-theme"', theme)
        self.assertIn('root.setAttribute("data-glz-appearance", value)', theme)
        self.assertIn('root.removeAttribute("data-glz-appearance")', theme)
        self.assertIn("applyRootAppearance(current);", theme)
        self.assertIn("DOMContentLoaded", theme)
        self.assertNotIn("hardwareConcurrency", theme)
        self.assertNotIn("deviceMemory", theme)

    def test_v16_accessibility_resilience_and_performance_fallbacks_are_source_controlled(self):
        css = self._read(APP_CSS) + "\n" + self._read(GLAZE_CSS)

        for contract in (
            "prefers-reduced-motion: reduce",
            "prefers-reduced-transparency: reduce",
            "prefers-contrast: more",
            "forced-colors: active",
            "@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))",
            "transition-duration: .01ms",
            "backdrop-filter: none",
            "outline: 2px solid Highlight",
            "text-size-adjust: 100%",
            "env(safe-area-inset-left)",
            "overscroll-behavior-inline: contain",
            "--glaze-effective-blur: 0px",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, css)

        for control in (
            "button:focus-visible",
            "input:focus-visible",
            "select:focus-visible",
            "textarea:focus-visible",
            "a:focus-visible",
        ):
            with self.subTest(control=control):
                self.assertIn(control, css)

    def test_user_interface_has_no_remote_browser_dependencies(self):
        sources = [
            BASE_TEMPLATE,
            APP_CSS,
            GLAZE_CSS,
            THEME_JS,
            MANAGER_MARK,
            *PRIMARY_TEMPLATES,
        ]

        for path in sources:
            text = self._read(path)
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                self.assertIsNone(
                    re.search(r"(?:src|href)=[\"']https?://", text, flags=re.IGNORECASE)
                )
                self.assertIsNone(
                    re.search(r"url\(\s*[\"']?https?://", text, flags=re.IGNORECASE)
                )
                self.assertNotIn("@import", text.lower())

    def test_manager_mark_is_static_and_script_free(self):
        mark = self._read(MANAGER_MARK).lower()

        self.assertIn("<svg", mark)
        self.assertNotIn("<script", mark)
        self.assertNotRegex(mark, r"(?:href|src)=[\"']https?://")

    def test_primary_surfaces_inherit_the_shared_glaze_shell(self):
        for template in PRIMARY_TEMPLATES:
            text = self._read(template)
            with self.subTest(template=template.name):
                self.assertIn('{% extends "core/base.html" %}', text)
