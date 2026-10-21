"""Read-only Docker health regression tests for the native Manager client."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from goreecloud_manager.infrastructure import _parse_docker


def fixture(containers):
    ps = []
    inspect = []
    for index, (name, state, health) in enumerate(containers):
        ident = f"fixture-{index:03d}"
        ps.append({"ID": ident, "Names": name, "Image": "synthetic/test", "State": state,
                   "Status": "Up 2 hours" if state == "running" else "Exited (0) 1 day ago"})
        info = {"Id": ident, "Name": "/" + name, "State": {"Status": state}}
        if health:
            info["State"]["Health"] = {"Status": health}
        inspect.append(info)
    return "\n".join([
        "__GCM_DOCKER_BEGIN__", "installed=1", "available=1", "version=fixture",
        "__GCM_DOCKER_PS__", *map(json.dumps, ps), "__GCM_DOCKER_STATS__",
        "__GCM_DOCKER_INSPECT__", *map(json.dumps, inspect), "__GCM_DOCKER_END__"
    ])


class DockerActiveHealthTests(unittest.TestCase):
    def test_exited_unhealthy_rollbacks_do_not_count_as_live_failures(self):
        data = fixture([
            ("running-web", "running", "healthy"),
            ("running-api", "running", "unhealthy"),
            ("old-rollback-a", "exited", "unhealthy"),
            ("old-rollback-b", "exited", "unhealthy"),
        ])
        overview = _parse_docker(data)
        self.assertEqual((overview.total, overview.running, overview.stopped), (4, 2, 2))
        self.assertEqual((overview.healthy, overview.unhealthy), (1, 1))
        self.assertEqual((overview.health_monitored, overview.no_healthcheck), (2, 0))
        self.assertEqual(sum(item.health == "unhealthy" for item in overview.containers), 3)

    def test_all_exited_historical_unhealthy_has_no_active_alert(self):
        overview = _parse_docker(fixture([
            ("old-rollback-a", "exited", "unhealthy"),
            ("old-rollback-b", "exited", "unhealthy"),
        ]))
        self.assertEqual((overview.running, overview.stopped, overview.unhealthy), (0, 2, 0))
        self.assertEqual((overview.health_monitored, overview.no_healthcheck), (0, 0))

    def test_running_without_healthcheck_counts_as_unmonitored(self):
        overview = _parse_docker(fixture([
            ("running-worker", "running", ""),
            ("running-service", "running", "starting"),
            ("old-rollback", "exited", "unhealthy"),
        ]))
        self.assertEqual((overview.health_starting, overview.unhealthy), (1, 0))
        self.assertEqual((overview.health_monitored, overview.no_healthcheck), (1, 1))


if __name__ == "__main__":
    unittest.main()
