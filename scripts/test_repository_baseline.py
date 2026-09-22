#!/usr/bin/env python3
"""Regression tests for the GoreeCloud Manager repository baseline validator."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from validate_repository_baseline import (
    LEGACY_FEATURE_ROADMAP,
    REQUIRED_REPOSITORY_CONTROLS,
    REQUIRED_ROOT_FILES,
    ROOT,
    validate_repository_baseline,
)


def copy_baseline(destination: Path) -> None:
    for relative in (*REQUIRED_ROOT_FILES, *REQUIRED_REPOSITORY_CONTROLS, "docs/glaze-ui.md"):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def expect_failure(root: Path, expected: str) -> None:
    try:
        validate_repository_baseline(root)
    except SystemExit as exc:
        if expected not in str(exc):
            raise AssertionError(f"expected {expected!r} in {exc!r}") from exc
    else:
        raise AssertionError("validator unexpectedly accepted an invalid repository baseline")


def main() -> None:
    validate_repository_baseline(ROOT)

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        copy_baseline(root)
        (root / "CAPABILITIES.md").unlink()
        expect_failure(root, "CAPABILITIES.md")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        copy_baseline(root)
        (root / "PLANNED-FEATURES.md").unlink()
        expect_failure(root, "PLANNED-FEATURES.md")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        copy_baseline(root)
        (root / LEGACY_FEATURE_ROADMAP).write_text("legacy roadmap must stay retired", encoding="utf-8")
        expect_failure(root, "retired FEATURE-ROADMAP.md")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        copy_baseline(root)
        manifest = root / "goreecloud.platform.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "repository: GoreeCloud/manager",
                "repository: GoreeCloud/goreecloud-manager",
            ),
            encoding="utf-8",
        )
        expect_failure(root, "stale repository identity")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        copy_baseline(root)
        manifest = root / "goreecloud.platform.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "glaze_ui_required: '1.6.0'",
                "glaze_ui_required: '1.5.1'",
            ),
            encoding="utf-8",
        )
        expect_failure(root, "glaze_ui_required: '1.6.0'")

    print("Manager repository baseline regression tests passed.")


if __name__ == "__main__":
    main()
