from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


def load_high_score_scripts() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    update_high_score = re.search(
        r"function updateHighScore\(\) \{.*?\n    \}",
        html,
        re.DOTALL,
    )
    update_score = re.search(
        r"function updateScore\(\) \{.*?\n    \}",
        html,
        re.DOTALL,
    )
    if not update_high_score or not update_score:
        msg = "Could not find score update functions in Snake_browser_game.html"
        raise AssertionError(msg)
    return f"{update_high_score.group(0)}\n{update_score.group(0)}"


def run_high_score_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        ["node", "-e", f"{load_high_score_scripts()}\n{script}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class HighScoreStorageTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_high_score_is_displayed_next_to_current_score(self):
        self.assertIn('<span class="scoreboard">', self.html)
        self.assertIn('<span>SCORE <span id="score">0</span></span>', self.html)
        self.assertIn('<span>HIGH <span id="highScore">0</span></span>', self.html)
        self.assertIn(".scoreboard {", self.html)
        self.assertIn("white-space: nowrap;", self.html)

    def test_high_score_is_loaded_and_saved_in_browser_storage(self):
        self.assertIn('const highScoreStorageKey = "snakeBrowserGameHighScore";', self.html)
        self.assertIn("const storage = browserEffects.createStorage(window.localStorage);", self.html)
        self.assertIn("let highScore = storage.loadNumber(highScoreStorageKey);", self.html)

    def test_score_update_promotes_only_new_high_score(self):
        result = run_high_score_script(
            textwrap.dedent(
                """
                let score = 40;
                let highScore = 30;
                const highScoreStorageKey = "snakeBrowserGameHighScore";
                const saves = [];
                const scoreElement = { textContent: "0" };
                const highScoreElement = { textContent: "30" };
                const storage = {
                  saveNumber(key, value) {
                    saves.push({ key, value });
                  }
                };

                updateScore();

                score = 15;
                updateScore();

                console.log(JSON.stringify({
                  scoreText: scoreElement.textContent,
                  highScoreText: highScoreElement.textContent,
                  highScore,
                  saves
                }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "scoreText": 15,
                "highScoreText": 40,
                "highScore": 40,
                "saves": [{"key": "snakeBrowserGameHighScore", "value": 40}],
            },
        )


if __name__ == "__main__":
    unittest.main()
