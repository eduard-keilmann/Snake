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

      gameTimer.clear();
      isRunning = true;
      isPaused = false;
      soundEffects.play("start");""",
            self.html,
        )
        self.assertIn(
            """if (tickResult.ateFood) {
        updateScore();
        soundEffects.play("food");""",
            self.html,
        )
        self.assertIn(
            """function endGame() {
      gameTimer.clear();
      isRunning = false;
      isPaused = false;
      isGameOver = true;
      soundEffects.play("gameOver");""",
            self.html,
        )
        self.assertIn('soundEffects.play("pause");', self.html)

    def test_sound_adapter_keeps_audio_resume_and_unlock_logic(self):
        self.assertIn("function createSoundEffects({ createAudioContext, sounds }) {", self.html)
        self.assertIn("function resume() {", self.html)
        self.assertIn("return currentAudioContext.resume().then(() => currentAudioContext);", self.html)
        self.assertIn(
            """if (soundEnabled) {
        soundEffects.resume().then(() => {
          soundEffects.play("start");
        });
      }""",
            self.html,
        )

    def test_audio_unlock_runs_on_first_page_gesture_for_ios(self):
        self.assertIn("let audioUnlocked = false;", self.html)
        self.assertIn("function unlock() {", self.html)
        self.assertIn("const silentBuffer = currentAudioContext.createBuffer(1, 1, 22050);", self.html)
        self.assertIn("silentSource.buffer = silentBuffer;", self.html)
        self.assertIn('soundEffects.unlock();', self.html)
        self.assertIn('document.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('document.addEventListener("touchstart", () => {', self.html)

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
      soundEffects.play("turn");
      return true;""",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
