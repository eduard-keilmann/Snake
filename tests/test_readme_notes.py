from pathlib import Path
import unittest


class ReadmeNotesTest(unittest.TestCase):
    def test_readme_matches_current_game_and_regression_scope(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("A simple retro Snake game implemented as a single HTML file.", readme)
        self.assertIn("High score is loaded from browser storage and updated when a run beats it.", readme)
        self.assertIn(
            "Restart: click once to pause and show confirmation, then confirm to restart or cancel to resume",
            readme,
        )
        self.assertIn(
            "Mobile: hold your finger down and swipe continuously anywhere on the page, tap the game field relative to the snake head, or use the on-screen direction buttons",
            readme,
        )
        self.assertIn(
            "Keep the game simple as a single-file browser game, but deepen behavior only where it improves Locality and Leverage.",
            readme,
        )
        self.assertIn("CONTEXT.local.md", readme)
        self.assertIn("tests/test_snake_game_rules.py", readme)
        self.assertIn("tests/test_input_command_seam.py", readme)
        self.assertIn("tests/test_browser_effect_adapters.py", readme)
        self.assertIn("tests/test_game_over_restart_behavior.py", readme)
        self.assertIn("tests/test_high_score_storage.py", readme)
        self.assertIn("tests/test_sound_feedback.py", readme)
        self.assertIn("tests/test_mobile_pad_layout.py", readme)
        self.assertNotIn("small mobile D-pad layout regression test", readme)


if __name__ == "__main__":
    unittest.main()
