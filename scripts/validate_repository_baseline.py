#!/usr/bin/env python3
"""Validate the mandatory GoreeCloud Manager repository baseline."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_WORKFLOW = ".github/workflows/repository-baseline.yml"
ROADMAP = "FEATURE-ROADMAP.md"

REQUIRED_ROOT_FILES = (
    "README.md",
    "SPECIFICATIONS.md",
    "FEATURES.md",
    "FEATURE-ROADMAP.md",
    "BENEFITS.md",
    "COMPETITIVE-OBJECTIVES.md",
    "BRANDING.md",
    "USER-MANUAL.md",
    "PRIVACY POLICY.md",
    "NOTES.md",
    "SECURITY.md",
    "CAPABILITIES.md",
    ".gitignore",
    ".editorconfig",
    "goreecloud.platform.yaml",
)
REQUIRED_REPOSITORY_CONTROLS = (
    ".github/PULL_REQUEST_TEMPLATE.md",
    BASELINE_WORKFLOW,
)
MINIMUM_MEANINGFUL_CHARACTERS = 20


def validate_repository_baseline(root: Path = ROOT) -> list[str]:
    validated: list[str] = []
    problems: list[str] = []

    for relative in (*REQUIRED_ROOT_FILES, *REQUIRED_REPOSITORY_CONTROLS):
        path = root / relative
        if not path.is_file():
            problems.append(f"missing required repository control: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            problems.append(f"required repository control is not UTF-8 text: {relative}")
            continue
        if len(text) < MINIMUM_MEANINGFUL_CHARACTERS:
            problems.append(f"required repository control is empty/placeholder-sized: {relative}")
            continue
        if text.lower() in {"todo", "tbd", "placeholder", "coming soon"}:
            problems.append(f"required repository control is a placeholder: {relative}")
            continue
        validated.append(relative)

    platform = root / "goreecloud.platform.yaml"
    if platform.is_file():
        text = platform.read_text(encoding="utf-8")
        for token in (
            "schema_version: '0.4'",
            "repository: GoreeCloud/manager",
            "platform_contract: '0.4'",
            "glaze_ui_required: '1.6.0'",
            "  policy:",
            "  observability:",
        ):
            if token not in text:
                problems.append(f"platform contract missing current stabilization token: {token}")
        if "repository: GoreeCloud/goreecloud-manager" in text:
            problems.append("platform contract contains stale repository identity GoreeCloud/goreecloud-manager")
        if "\n  sync:" in text:
            problems.append("GoreeCloud Sync must remain separately governed, not a tenth Integral Platform System")

    roadmap = root / ROADMAP
    if roadmap.is_file():
        text = roadmap.read_text(encoding="utf-8")
        if "**Canonical repository:** `GoreeCloud/manager`" not in text:
            problems.append("feature roadmap does not identify canonical repository GoreeCloud/manager")
        if "GoreeCloud/goreecloud-manager" in text:
            problems.append("feature roadmap contains stale repository identity GoreeCloud/goreecloud-manager")

    branding = root / "BRANDING.md"
    if branding.is_file():
        text = branding.read_text(encoding="utf-8")
        if "GoreeCloud/branding-assets" not in text:
            problems.append("branding record does not identify canonical GoreeCloud/branding-assets authority")
        if "GoreeCloud/goreecloud-branding-assets" in text:
            problems.append("branding record contains stale branding repository identity")

    glaze = root / "docs/glaze-ui.md"
    if glaze.is_file():
        text = glaze.read_text(encoding="utf-8")
        for token in (
            "implemented source mapping is **Glaze UI 1.3.0**",
            "current shared Stable consumer target is **Glaze UI 1.6.0**",
            "migration-required",
        ):
            if token not in text:
                problems.append(f"Glaze UI record missing truthful current-target boundary: {token}")

    workflow = root / BASELINE_WORKFLOW
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        for token in (
            "persist-credentials: false",
            "Verify exact source revision",
            'run: test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"',
            "Validate repository documentation baseline",
            "Test repository documentation baseline",
        ):
            if token not in text:
                problems.append(f"baseline workflow missing stabilization control: {token}")

    if problems:
        raise SystemExit("Manager repository baseline validation failed: " + "; ".join(problems))
    return validated


def main() -> None:
    validated = validate_repository_baseline()
    print(
        "Manager repository baseline passed: "
        f"mandatory_root={len(REQUIRED_ROOT_FILES)}, "
        f"conditional_controls={len(REQUIRED_REPOSITORY_CONTROLS)}, "
        f"validated={len(validated)}."
    )


if __name__ == "__main__":
    main()
