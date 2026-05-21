from pathlib import Path
import unittest


class SoundFeedbackTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_gameplay_events_play_retro_sound_effects(self):
        self.assertIn(
            """function startGame() {
      if (isGameOver) {
        resetGame();
      }

      clearInterval(gameInterval);
      isRunning = true;
      isPaused = false;
      playSound("start");""",
            self.html,
        )
        self.assertIn(
            """if (head.x === food.x && head.y === food.y) {
        score += 10;
        updateScore();
        playSound("food");""",
            self.html,
        )
        self.assertIn(
            """function endGame() {
      clearInterval(gameInterval);
      isRunning = false;
      isPaused = false;
      isGameOver = true;
      playSound("gameOver");""",
            self.html,
        )
        self.assertIn('playSound("pause");', self.html)

    def test_turn_sound_only_plays_after_accepted_direction_change(self):
        self.assertIn("const isSameAsNext =", self.html)
        self.assertIn(
            """if (!isOpposite && !isSameAsNext) {
        nextDirection = chosen;
        playSound("turn");
      }""",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
