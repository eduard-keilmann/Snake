from pathlib import Path
import unittest


class MobilePadLayoutTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_d_pad_controls_are_compact_for_mobile_play(self):
        self.assertIn("position: relative;", self.html)
        self.assertIn("width: 140px;", self.html)
        self.assertIn("height: 140px;", self.html)
        self.assertIn("width: 56px;", self.html)
        self.assertIn("height: 56px;", self.html)
        self.assertIn("left: 42px;", self.html)
        self.assertIn("top: 0;", self.html)
        self.assertIn("top: 42px;", self.html)
        self.assertIn("top: 84px;", self.html)

    def test_action_buttons_have_space_below_d_pad(self):
        self.assertIn("margin-top: 14px;", self.html)

    def test_restart_button_requires_second_click(self):
        self.assertIn("let restartConfirmationPending = false;", self.html)
        self.assertIn("let restartConfirmationWasRunning = false;", self.html)
        self.assertIn("function requestRestart()", self.html)
        self.assertIn("function cancelRestartConfirmation()", self.html)
        self.assertIn("clearInterval(gameInterval);", self.html)
        self.assertIn('showOverlay("RESTART?", "Confirm restart or cancel to resume.", "CONFIRM");', self.html)
        self.assertIn('pauseButton.textContent = "CANCEL";', self.html)
        self.assertIn('restartButton.textContent = "CONFIRM";', self.html)
        self.assertIn('cancelButton.classList.remove("hidden");', self.html)
        self.assertIn('cancelButton.addEventListener("click", cancelRestartConfirmation);', self.html)
        self.assertIn('restartButton.addEventListener("click", requestRestart);', self.html)


if __name__ == "__main__":
    unittest.main()
