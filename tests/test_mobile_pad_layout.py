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
        self.assertIn("Square fallback: width: min(260px, 76vw, 34dvh); aspect-ratio: 1;", self.html)
        self.assertIn("width: min(300px, 86vw, 39dvh);", self.html)
        self.assertIn("aspect-ratio: 1.30 / 1;", self.html)
        self.assertIn("width: 100%;", self.html)
        self.assertIn("height: 100%;", self.html)
        self.assertIn("--pad-button-offset-x: 0px;", self.html)
        self.assertIn("transform: translateX(var(--pad-button-offset-x));", self.html)
        self.assertIn("--pad-button-offset-x: -4px;", self.html)
        self.assertIn("--pad-button-offset-x: 4px;", self.html)
        self.assertIn("touch-action: none;", self.html)
        self.assertIn("-webkit-user-select: none;", self.html)
        self.assertIn("grid-column: 2;", self.html)
        self.assertIn("grid-row: 1;", self.html)
        self.assertIn("grid-column: 1;", self.html)
        self.assertIn("grid-row: 2;", self.html)
        self.assertIn("grid-column: 3;", self.html)
        self.assertIn("grid-row: 3;", self.html)
        self.assertIn(".mobile-pad button:active", self.html)
        self.assertIn("transform: translateX(var(--pad-button-offset-x)) scale(0.90);", self.html)
        self.assertIn("--button-active-glow: rgba(190, 255, 118, 0.85);", self.html)
        self.assertIn("box-shadow 110ms ease-out", self.html)
        self.assertIn("inset 0 0 0 3px var(--button-active-glow)", self.html)
        self.assertIn("0 0 18px 7px rgba(190, 255, 118, 0.42)", self.html)

    def test_d_pad_buttons_have_accessible_direction_names(self):
        self.assertIn('aria-label="Move up"', self.html)
        self.assertIn('aria-label="Move left"', self.html)
        self.assertIn('aria-label="Move right"', self.html)
        self.assertIn('aria-label="Move down"', self.html)

    def test_help_text_mentions_continuous_swipe_control(self):
        self.assertIn("Use arrow keys, WASD, continuous swipe, or buttons.", self.html)
        self.assertIn(
            "Mobile: Hold finger down and swipe continuously, or use buttons",
            self.html,
        )

    def test_sound_toggle_is_visible_and_documented(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn('<button id="soundButton" aria-pressed="true">SOUND ON</button>', self.html)
        self.assertIn("Sound: optional retro-style effects for turns, food, pause/start, and game over", readme)

    def test_sound_is_browser_generated_and_user_toggle_controlled(self):
        self.assertIn("const AudioContextConstructor = window.AudioContext || window.webkitAudioContext;", self.html)
        self.assertIn("let soundEnabled = true;", self.html)
        self.assertIn("function toggleSound()", self.html)
        self.assertIn('soundButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('soundButton.textContent = soundEnabled ? "SOUND ON" : "SOUND OFF";', self.html)
        self.assertNotIn("<audio", self.html)
        self.assertNotIn(".mp3", self.html)
        self.assertNotIn(".wav", self.html)

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
        self.assertIn("const swipeThreshold = 24;", self.html)
        self.assertIn("let touchLastX = null;", self.html)
        self.assertIn("let touchLastY = null;", self.html)
        self.assertIn("function applySwipeDirection(newDirection)", self.html)
        self.assertIn("function handleSwipeMovement(clientX, clientY)", self.html)
        self.assertIn('document.addEventListener("touchstart"', self.html)
        self.assertIn('document.addEventListener("touchmove"', self.html)
        self.assertIn('document.addEventListener("touchend"', self.html)
        self.assertIn('document.addEventListener("touchcancel"', self.html)
        self.assertNotIn('canvas.addEventListener("touchstart"', self.html)
        self.assertNotIn('canvas.addEventListener("touchmove"', self.html)
        self.assertNotIn('canvas.addEventListener("touchend"', self.html)

    def test_lcd_tap_zones_turn_snake_without_breaking_swipe(self):
        self.assertIn("let touchStartX = null;", self.html)
        self.assertIn("let touchStartY = null;", self.html)
        self.assertIn("let touchStartedOnCanvas = false;", self.html)
        self.assertIn("let swipeDirectionApplied = false;", self.html)
        self.assertIn("function getTapDirection(clientX, clientY)", self.html)
        self.assertIn("const rect = canvas.getBoundingClientRect();", self.html)
        self.assertIn("const centerX = rect.left + rect.width / 2;", self.html)
        self.assertIn("const centerY = rect.top + rect.height / 2;", self.html)
        self.assertIn("const deltaX = clientX - centerX;", self.html)
        self.assertIn("const deltaY = clientY - centerY;", self.html)
        self.assertIn("Math.abs(deltaX) > Math.abs(deltaY)", self.html)
        self.assertNotIn("const head = snake[0];", self.html)
        self.assertIn("function applyTapDirection(newDirection)", self.html)
        self.assertIn("if (setDirection(newDirection)) {\n        showTapFeedback(newDirection);\n      }", self.html)
        self.assertIn("function handleTapZone(clientX, clientY)", self.html)
        self.assertIn("if (!touchStartedOnCanvas || swipeDirectionApplied)", self.html)
        self.assertIn("const movedTooFar =", self.html)
        self.assertIn("applyTapDirection(getTapDirection(clientX, clientY));", self.html)
        self.assertIn('const isButtonTouch = event.target.closest("button") !== null;', self.html)
        self.assertNotIn('document.addEventListener("pointerdown", event => {', self.html)

    def test_lcd_tap_zones_show_brief_direction_feedback(self):
        self.assertIn("let tapFeedbackDirection = null;", self.html)
        self.assertIn("let tapFeedbackTimeout;", self.html)
        self.assertIn("function drawTapFeedback()", self.html)
        self.assertIn("if (!tapFeedbackDirection) return;", self.html)
        self.assertIn("drawTapFeedback();", self.html)
        self.assertIn("function showTapFeedback(newDirection)", self.html)
        self.assertIn("tapFeedbackDirection = newDirection;", self.html)
        self.assertIn("clearTimeout(tapFeedbackTimeout);", self.html)
        self.assertIn("tapFeedbackTimeout = setTimeout(() => {", self.html)
        self.assertIn("tapFeedbackDirection = null;", self.html)
        self.assertIn("drawGame();", self.html)

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
