from pathlib import Path
import unittest


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
        self.assertIn('const highScoreElement = document.getElementById("highScore");', self.html)
        self.assertIn("let highScore = loadHighScore();", self.html)
        self.assertIn("function loadHighScore()", self.html)
        self.assertIn("localStorage.getItem(highScoreStorageKey)", self.html)
        self.assertIn("Number.isFinite(storedHighScore) && storedHighScore > 0", self.html)
        self.assertIn("function saveHighScore()", self.html)
        self.assertIn("localStorage.setItem(highScoreStorageKey, String(highScore));", self.html)
        self.assertIn("} catch {\n        return 0;\n      }", self.html)

    def test_score_update_promotes_new_high_score(self):
        self.assertIn("function updateHighScore()", self.html)
        self.assertIn("if (score <= highScore) return;", self.html)
        self.assertIn("highScore = score;", self.html)
        self.assertIn("highScoreElement.textContent = highScore;", self.html)
        self.assertIn("saveHighScore();", self.html)
        self.assertIn(
            """function updateScore() {
      scoreElement.textContent = score;
      highScoreElement.textContent = highScore;
      updateHighScore();
    }""",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
