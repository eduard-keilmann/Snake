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
            """if (tickResult.ateFood) {
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

    def test_sound_unlock_waits_for_browser_audio_resume(self):
        self.assertIn("function resumeAudioContext()", self.html)
        self.assertIn("return audioContext.resume().then(() => audioContext);", self.html)
        self.assertIn(
            """if (soundEnabled) {
        resumeAudioContext().then(() => {
          playSound("start");
        });
      }""",
            self.html,
        )

    def test_audio_unlock_runs_on_first_page_gesture_for_ios(self):
        self.assertIn("let audioUnlocked = false;", self.html)
        self.assertIn("function unlockAudio()", self.html)
        self.assertIn("const silentBuffer = audioContext.createBuffer(1, 1, 22050);", self.html)
        self.assertIn("silentSource.buffer = silentBuffer;", self.html)
        self.assertIn('document.addEventListener("pointerdown", unlockAudio, { capture: true });', self.html)
        self.assertIn('document.addEventListener("touchstart", unlockAudio, { capture: true, passive: true });', self.html)

    def test_retro_tones_are_loud_enough_for_phone_speakers(self):
        self.assertIn("function playTone(frequency, startDelay = 0, duration = 0.06, volume = 0.09)", self.html)
        self.assertIn("turn: [{ frequency: 880, delay: 0, duration: 0.035, volume: 0.08 }]", self.html)
        self.assertIn("pause: [{ frequency: 392, delay: 0, duration: 0.08, volume: 0.09 }]", self.html)

    def test_turn_sound_only_plays_after_accepted_direction_change(self):
        self.assertIn("const isOpposite =", self.html)
        self.assertIn("const isSameAsNext =", self.html)
        self.assertIn(
            """if (isOpposite || isSameAsNext) {
        return false;
      }""",
            self.html,
        )
        self.assertIn(
            """nextDirection = chosen;
      playSound("turn");
      return true;""",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
