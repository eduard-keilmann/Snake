from pathlib import Path
import unittest


class MobilePadLayoutTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_d_pad_controls_are_compact_for_mobile_play(self):
        self.assertIn("display: grid;", self.html)
        self.assertIn("grid-template-columns: repeat(3, 1fr);", self.html)
        self.assertIn("grid-template-rows: repeat(3, 1fr);", self.html)
        self.assertIn("gap: min(8px, 2vw);", self.html)
        self.assertIn("width: min(260px, 76vw, 34dvh);", self.html)
        self.assertIn("aspect-ratio: 1;", self.html)
        self.assertIn("width: 100%;", self.html)
        self.assertIn("height: 100%;", self.html)
        self.assertIn("touch-action: none;", self.html)
        self.assertIn("-webkit-user-select: none;", self.html)
        self.assertIn("grid-column: 2;", self.html)
        self.assertIn("grid-row: 1;", self.html)
        self.assertIn("grid-column: 1;", self.html)
        self.assertIn("grid-row: 2;", self.html)
        self.assertIn("grid-column: 3;", self.html)
        self.assertIn("grid-row: 3;", self.html)
        self.assertIn(".mobile-pad button:active", self.html)
        self.assertIn("transform: scale(0.90);", self.html)
        self.assertIn("--button-active-glow: rgba(190, 255, 118, 0.85);", self.html)
        self.assertIn("box-shadow 110ms ease-out", self.html)
        self.assertIn("inset 0 0 0 3px var(--button-active-glow)", self.html)
        self.assertIn("0 0 18px 7px rgba(190, 255, 118, 0.42)", self.html)

    def test_d_pad_buttons_have_accessible_direction_names(self):
        self.assertIn('aria-label="Move up"', self.html)
        self.assertIn('aria-label="Move left"', self.html)
        self.assertIn('aria-label="Move right"', self.html)
        self.assertIn('aria-label="Move down"', self.html)

    def test_action_buttons_are_below_d_pad_on_mobile(self):
        self.assertIn("@media (max-width: 759px)", self.html)
        self.assertNotIn("order: -1;", self.html)
        self.assertIn("margin-top: 16px;", self.html)

    def test_mobile_page_cannot_scroll(self):
        self.assertIn("min-height: 100dvh;", self.html)
        self.assertIn("height: 100dvh;", self.html)
        self.assertIn("overflow: hidden;", self.html)
        self.assertIn(
            "padding-bottom: max(10px, calc(10px + env(safe-area-inset-bottom)));",
            self.html,
        )
        self.assertIn("touch-action: none;", self.html)

    def test_swipe_controls_are_bound_to_whole_page(self):
        self.assertIn('document.addEventListener("touchstart"', self.html)
        self.assertIn('document.addEventListener("touchend"', self.html)
        self.assertNotIn('canvas.addEventListener("touchstart"', self.html)
        self.assertNotIn('canvas.addEventListener("touchend"', self.html)

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
