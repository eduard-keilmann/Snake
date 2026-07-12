from __future__ import annotations

from pathlib import Path
import re
import unittest


HTML = Path("Snake_browser_game.html").read_text(encoding="utf-8")


class OnlineLeaderboardTest(unittest.TestCase):
    def test_sound_and_highscore_controls_are_above_the_game_screen(self):
        actions = re.search(
            r'<div class="screen-actions">(?P<controls>[\s\S]*?)</div>\s*<section class="screen"',
            HTML,
        )

        self.assertIsNotNone(actions)
        self.assertIn('id="soundButton"', actions.group("controls"))
        self.assertRegex(actions.group("controls"), r'data-action="leaderboard"[^>]*hidden')
        self.assertNotRegex(
            re.search(r'<div class="screen-top">(?P<top>[\s\S]*?)</div>', HTML).group("top"),
            r'id="soundButton"',
        )

    def test_online_leaderboard_is_optional_and_uses_the_local_worker(self):
        self.assertIn('"http://localhost:8787"', HTML)
        self.assertIn("AbortSignal.timeout(10000)", HTML)
        self.assertIn("leaderboardButton.hidden = !leaderboardAvailable", HTML)

    def test_a_new_run_requests_a_ticket_and_game_over_offers_a_score(self):
        restart_game = re.search(r"function restartGame\(\) \{(?P<body>[\s\S]*?)\n    \}", HTML)
        end_game = re.search(r"function endGame\(\) \{(?P<body>[\s\S]*?)\n    \}", HTML)

        self.assertIsNotNone(restart_game)
        self.assertIsNotNone(end_game)
        self.assertIn("requestOnlineRunTicket();", restart_game.group("body"))
        self.assertIn("offerOnlineScoreEntry();", end_game.group("body"))

    def test_open_dialog_keeps_name_keystrokes_out_of_game_controls(self):
        self.assertRegex(
            HTML,
            re.compile(
                r'document\.addEventListener\("keydown", event => \{\s*if \(leaderboardDialog\.open\) return;'
            ),
        )

    def test_failed_refresh_after_score_submission_keeps_highscores_button(self):
        submit_handler = re.search(
            r'leaderboardScoreForm\.addEventListener\("submit", async event => \{(?P<body>[\s\S]*?)\n    \}\);',
            HTML,
        )

        self.assertIsNotNone(submit_handler)
        self.assertIn("await refreshOnlineLeaderboard(false);", submit_handler.group("body"))


if __name__ == "__main__":
    unittest.main()
