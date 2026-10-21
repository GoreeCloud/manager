"""Regression checks for live vs historical Docker health reporting.

Extract just the parser's pure stdlib-backed definitions: Django CI does not
install the optional native desktop GUI dependencies.
"""
import ast
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any
from unittest import TestCase

SOURCE = Path(__file__).resolve().parent.parent / "desktop-client" / "goreecloud_manager" / "infrastructure.py"


def _parser():
    content = SOURCE.read_text(encoding="utf-8")
    selected = {"ContainerInfo", "DockerOverview", "_section", "_kv_lines", "_parse_json_lines", "_pick", "_parse_docker"}
    statements = []
    for node in ast.parse(content).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in selected:
            statements.append(ast.get_source_segment(content, node))
    scope = {"dataclass": dataclass, "field": field, "json": json, "Any": Any}
    exec("\n\n".join(statements), scope)
    return scope["_parse_docker"]


def _sample(*entries):
    rows = []
    inspected = []
    for name, state, health in entries:
        status = state.title() + (f" ({health})" if health else "")
        rows.append(json.dumps({"Names": name, "ID": name, "Image": "example:latest", "State": state, "Status": status}))
        inspected.append(json.dumps({"Id": name, "Name": "/" + name, "State": {"Status": state, "Health": {"Status": health} if health else {}}}))
    return (
        "__GCM_DOCKER_BEGIN__\ninstalled=1\navailable=1\nversion=test\n"
        "__GCM_DOCKER_PS__\n" + "\n".join(rows) + "\n"
        "__GCM_DOCKER_STATS__\n__GCM_DOCKER_INSPECT__\n"
        + "\n".join(inspected) + "\n__GCM_DOCKER_END__"
    )


class DesktopDockerHealthRegressionTests(TestCase):
    def test_exited_rollback_container_does_not_raise_active_unhealthy_alert(self):
        overview = _parser()(_sample(("rollback", "exited", "unhealthy")))
        self.assertEqual(overview.total, 1)
        self.assertEqual(overview.stopped, 1)
        self.assertEqual(overview.running, 0)
        self.assertEqual(overview.unhealthy, 0)
        self.assertEqual(overview.health_monitored, 0)
        self.assertEqual(overview.no_healthcheck, 0)
        self.assertEqual(overview.containers[0].health, "unhealthy")

    def test_active_health_check_counts_are_independent_of_stopped_history(self):
        overview = _parser()(_sample(
            ("healthy", "running", "healthy"),
            ("active_problem", "running", "unhealthy"),
            ("unchecked", "running", ""),
            ("rollback", "exited", "unhealthy"),
        ))
        self.assertEqual((overview.running, overview.stopped, overview.total), (3, 1, 4))
        self.assertEqual((overview.healthy, overview.unhealthy, overview.no_healthcheck), (1, 1, 1))
        self.assertEqual(overview.health_monitored, 2)

    def test_ui_filters_do_not_confuse_stopped_history_with_current_issues(self):
        ui = (SOURCE.parent / "ui.py").read_text(encoding="utf-8")
        self.assertIn('active_health = health if state == "running" else ""', ui)
        self.assertIn('mode == "unhealthy" and active_health != "unhealthy"', ui)
        self.assertIn('mode == "attention" and not (active_health', ui)
        self.assertIn('f"Last: {item.health.casefold()}"', ui)
