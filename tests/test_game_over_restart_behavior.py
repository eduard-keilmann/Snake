from pathlib import Path
import unittest


class GameOverRestartBehaviorTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_starting_after_game_over_resets_stale_game_state(self):
        self.assertIn("let isGameOver;", self.html)
        self.assertIn("isGameOver = false;", self.html)
        self.assertIn("isGameOver = true;", self.html)
        self.assertIn(
            """function startGame() {
      if (isGameOver) {
        resetGame();
      }""",
            self.html,
        )

    def test_mobile_direction_buttons_start_clean_state_before_turning(self):
        self.assertIn(
            """button.addEventListener("pointerdown", () => {
        vibrate();
        if (!isRunning) {
          startGame();
        }
        setDirection(button.dataset.direction);""",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
