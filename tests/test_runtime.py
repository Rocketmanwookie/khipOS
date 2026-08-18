from pathlib import Path
import tempfile
import unittest

from ai_os.agents import route_agent
from ai_os.runtime import Runtime


class RouterTests(unittest.TestCase):
    def test_routes_specialists(self):
        self.assertEqual(route_agent("build an Excel workbook").agent_id, "spreadsheet")
        self.assertEqual(route_agent("make a FreeCAD panel layout").agent_id, "cad")
        self.assertEqual(route_agent("debug this Python app").agent_id, "code")


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.runtime = Runtime(Path(self.temp.name), workspace_root=Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def test_project_round_trip(self):
        created = self.runtime.create_project("PLC Monitor")
        self.assertEqual(self.runtime.list_projects()[0]["project_id"], created["project_id"])

    def test_safe_intent_has_no_approval(self):
        result = self.runtime.handle_intent("draft a project memo")
        self.assertEqual(result["agent"]["agent_id"], "writing")
        self.assertIsNone(result["approval"])

    def test_sensitive_intent_requires_approval(self):
        result = self.runtime.handle_intent("send the report")
        self.assertEqual(result["approval"]["payload"]["status"], "pending")

    def test_empty_intent_is_rejected(self):
        with self.assertRaises(ValueError):
            self.runtime.handle_intent(" ")

    def test_workspace_explorer_lists_entries_without_git_noise(self):
        (Path(self.temp.name) / "alpha.txt").write_text("alpha", encoding="utf-8")
        (Path(self.temp.name) / "zeta").mkdir()
        (Path(self.temp.name) / ".git").mkdir()

        result = self.runtime.explore_workspace()

        names = [entry["name"] for entry in result["listing"]["entries"]]
        self.assertEqual(names, ["projects", "zeta", "alpha.txt"])
        self.assertEqual(result["context"]["packet_type"], "ContextFrame")
        self.assertEqual(result["context"]["payload"]["permission"], "observe")

    def test_workspace_explorer_rejects_path_escape(self):
        with self.assertRaises(ValueError):
            self.runtime.explore_workspace("../")


if __name__ == "__main__":
    unittest.main()
