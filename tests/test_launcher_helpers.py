"""Small regression tests for UniGame Launcher's pure helper functions."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "UniGameLauncher_v1_2.py"
SPEC = importlib.util.spec_from_file_location("unigamelauncher_source", SOURCE)
assert SPEC and SPEC.loader
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


class LauncherHelperTests(unittest.TestCase):
    def test_format_time_handles_minutes_and_hours(self):
        self.assertEqual(launcher.format_time(59), "0m")
        self.assertEqual(launcher.format_time(3600), "1h 0m")
        self.assertEqual(launcher.format_time(3720), "1h 2m")

    def test_default_profile_has_expected_collections(self):
        profile = launcher.default_profile("Test")
        self.assertEqual(profile["name"], "Test")
        self.assertEqual(profile["games"], [])
        self.assertEqual(profile["wishlist"], [])

    def test_default_data_has_player_profile(self):
        data = launcher.default_data()
        self.assertEqual(data["active_profile"], "Player")
        self.assertIn("Player", data["profiles"])

    def test_json_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            original = {"games": [{"title": "Example"}]}
            launcher.save_json(path, original)
            self.assertEqual(launcher.load_json(path, {}), original)


if __name__ == "__main__":
    unittest.main()
