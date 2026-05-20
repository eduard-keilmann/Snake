from pathlib import Path
import unittest


class MobilePadLayoutTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_d_pad_controls_are_compact_for_mobile_play(self):
        self.assertIn("display: grid;", self.html)
        self.assertIn("grid-template-columns: repeat(3, 1fr);", self.html)
        self.assertIn("grid-template-rows: repeat(3, 1fr);", self.html)
        self.assertIn("gap: min(12px, 3vw);", self.html)
        self.assertIn("width: min(240px, 72vw);", self.html)
        self.assertIn("aspect-ratio: 1;", self.html)
        self.assertIn("width: 100%;", self.html)
        self.assertIn("height: 100%;", self.html)
        self.assertIn("touch-action: manipulation;", self.html)
        self.assertIn("-webkit-user-select: none;", self.html)
        self.assertIn("grid-column: 2;", self.html)
        self.assertIn("grid-row: 1;", self.html)
        self.assertIn("grid-column: 1;", self.html)
        self.assertIn("grid-row: 2;", self.html)
        self.assertIn("grid-column: 3;", self.html)
        self.assertIn("grid-row: 3;", self.html)
        self.assertIn(".mobile-pad button:active", self.html)
        self.assertIn("transform: scale(0.90);", self.html)

    def test_d_pad_buttons_have_accessible_direction_names(self):
        self.assertIn('aria-label="Move up"', self.html)
        self.assertIn('aria-label="Move left"', self.html)
        self.assertIn('aria-label="Move right"', self.html)
        self.assertIn('aria-label="Move down"', self.html)

    def test_action_buttons_have_space_below_d_pad(self):
        self.assertIn("@media (max-width: 759px)", self.html)
        self.assertIn("margin-top: 32px;", self.html)

    def test_restart_button_requires_second_click(self):
        self.assertIn("let restartConfirmationPending = false;", self.html)
        self.assertIn("let restartConfirmationWasRunning = false;", self.html)
        self.assertIn("function requestRestart()", self.html)
        self.assertIn("function cancelRestartConfirmation()", self.html)
        self.assertIn("clearInterval(gameInterval);", self.html)
        self.assertIn('showOverlay("RESTART?", "Confirm restart or cancel to resume.", "CONFIRM");', self.html)
        self.assertIn('pauseButton.textContent = "CANCEL";', self.html)
        self.assertIn('restartButton.textContent = "CONFIRM";', self.html)
        self.assertIn("restartButton.style.order = 1;", self.html)
        self.assertIn("pauseButton.style.order = 2;", self.html)
        self.assertIn('cancelButton.classList.remove("hidden");', self.html)
        self.assertIn('cancelButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn("cancelRestartConfirmation();", self.html)
        self.assertIn('restartButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn("requestRestart();", self.html)

    def test_mobile_buttons_trigger_haptic_feedback_when_supported(self):
        self.assertIn("function vibrate(pattern = 12)", self.html)
        self.assertIn("if (!navigator.vibrate) return;", self.html)
        self.assertIn("navigator.vibrate(pattern);", self.html)
        self.assertIn("vibrate();", self.html)
        self.assertIn("vibrate([18, 40, 18]);", self.html)
        self.assertIn('button.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('startButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('pauseButton.addEventListener("pointerdown", () => {', self.html)


if __name__ == "__main__":
    unittest.main()
