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
        self.assertIn("width: min(330px, 94vw, 42.9dvh);", self.html)
        self.assertIn("aspect-ratio: 1.55 / 1;", self.html)
        self.assertIn("width: 100%;", self.html)
        self.assertIn("height: 100%;", self.html)
        self.assertIn("--pad-button-offset-x: 0px;", self.html)
        self.assertIn("--pad-button-scale-x: 1;", self.html)
        self.assertIn(
            "transform: translateX(var(--pad-button-offset-x)) scaleX(var(--pad-button-scale-x));",
            self.html,
        )
        self.assertIn("transform-origin: center;", self.html)
        self.assertIn("--pad-button-offset-x: 2px;", self.html)
        self.assertIn("--pad-button-offset-x: -2px;", self.html)
        self.assertIn("touch-action: none;", self.html)
        self.assertIn("-webkit-user-select: none;", self.html)
        self.assertIn("grid-column: 2;", self.html)
        self.assertIn("grid-row: 1;", self.html)
        self.assertIn(".mobile-pad .up,\n    .mobile-pad .down", self.html)
        self.assertIn("--pad-button-scale-x: 1.52;", self.html)
        self.assertIn(".mobile-pad .left,\n    .mobile-pad .right", self.html)
        self.assertIn("--pad-button-scale-x: 1.12;", self.html)
        self.assertIn("justify-self: center;", self.html)
        self.assertIn("grid-column: 1;", self.html)
        self.assertIn("grid-row: 2;", self.html)
        self.assertIn("grid-column: 3;", self.html)
        self.assertIn("grid-row: 3;", self.html)
        self.assertIn(".mobile-pad button:active", self.html)
        self.assertIn(
            "transform: translateX(var(--pad-button-offset-x)) scaleX(var(--pad-button-scale-x)) scale(0.90);",
            self.html,
        )
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

    def test_top_action_buttons_use_one_readable_size(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn('<button id="soundButton" aria-pressed="true">SOUND</button>', self.html)
        self.assertIn('data-action="leaderboard" hidden>HIGHSCORES</button>', self.html)
        self.assertIn(".screen-actions button {", self.html)
        self.assertIn("padding: 8px 12px;", self.html)
        self.assertIn("font-size: 0.82rem;", self.html)
        self.assertIn("#soundButton {", self.html)
        self.assertIn('color: #1f4f1f;', self.html)
        self.assertIn('#soundButton[aria-pressed="false"] {', self.html)
        self.assertIn("Sound: optional retro-style effects for turns, food, pause/start, and game over", readme)

    def test_mobile_game_field_has_more_height_without_exceeding_viewport_width(self):
        self.assertIn("padding: 10px 2px;", self.html)
        self.assertIn(
            "width: min(calc(100vw - 4px), 420px, max(220px, calc(100dvh - 370px)));",
            self.html,
        )

    def test_sound_is_browser_generated_and_user_toggle_controlled(self):
        self.assertIn("const AudioContextConstructor = window.AudioContext || window.webkitAudioContext;", self.html)
        self.assertIn("let soundEnabled = true;", self.html)
        self.assertIn("function toggleSound()", self.html)
        self.assertIn('soundButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('soundButton.textContent = "SOUND";', self.html)
        self.assertIn('soundButton.setAttribute("aria-pressed", String(soundEnabled));', self.html)
        self.assertNotIn("<audio", self.html)
        self.assertNotIn(".mp3", self.html)
        self.assertNotIn(".wav", self.html)

    def test_action_buttons_are_below_d_pad_on_mobile(self):
        self.assertIn("@media (max-width: 759px)", self.html)
        self.assertNotIn("order: -1;", self.html)
        self.assertIn("margin-top: 8px;", self.html)

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
        self.assertIn("const canvasX = ((clientX - rect.left) / rect.width) * canvas.width;", self.html)
        self.assertIn("const canvasY = ((clientY - rect.top) / rect.height) * canvas.height;", self.html)
        self.assertIn("const head = snake[0];", self.html)
        self.assertIn("const headCenterX = head.x * gridSize + gridSize / 2;", self.html)
        self.assertIn("const headCenterY = head.y * gridSize + gridSize / 2;", self.html)
        self.assertIn("const deltaX = canvasX - headCenterX;", self.html)
        self.assertIn("const deltaY = canvasY - headCenterY;", self.html)
        self.assertIn("Math.abs(deltaX) > Math.abs(deltaY)", self.html)
        self.assertNotIn("const centerX = rect.left + rect.width / 2;", self.html)
        self.assertNotIn("const centerY = rect.top + rect.height / 2;", self.html)
        self.assertIn("function applyTapDirection(newDirection)", self.html)
        self.assertIn("handleInputCommand(inputCommands.move(newDirection));", self.html)
        self.assertIn("function handleTapZone(clientX, clientY)", self.html)
        self.assertIn("if (!touchStartedOnCanvas || swipeDirectionApplied)", self.html)
        self.assertIn("const movedTooFar =", self.html)
        self.assertIn("applyTapDirection(getTapDirection(clientX, clientY));", self.html)
        self.assertIn('const isButtonTouch = event.target.closest("button") !== null;', self.html)
        self.assertNotIn('document.addEventListener("pointerdown", event => {', self.html)

    def test_lcd_tap_zones_do_not_show_triangle_feedback(self):
        self.assertNotIn("let tapFeedbackDirection", self.html)
        self.assertNotIn("let tapFeedbackTimeout", self.html)
        self.assertNotIn("function drawTapFeedback()", self.html)
        self.assertNotIn("function showTapFeedback", self.html)
        self.assertNotIn("drawTapFeedback();", self.html)

    def test_restart_button_requires_second_click(self):
        self.assertIn("let restartConfirmationPending = false;", self.html)
        self.assertIn("let restartConfirmationWasRunning = false;", self.html)
        self.assertIn("function requestRestart()", self.html)
        self.assertIn("function cancelRestartConfirmation()", self.html)
        self.assertIn("gameTimer.clear();", self.html)
        self.assertIn('overlayEffects.show("RESTART?", "Confirm restart or cancel to resume.", "CONFIRM");', self.html)
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
        self.assertIn("function createVibration({ vibrate }) {", self.html)
        self.assertIn("if (!vibrate) return false;", self.html)
        self.assertIn("vibrate(pattern);", self.html)
        self.assertIn("vibration.run();", self.html)
        self.assertIn("vibration.run([18, 40, 18]);", self.html)
        self.assertIn('button.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('startButton.addEventListener("pointerdown", () => {', self.html)
        self.assertIn('pauseButton.addEventListener("pointerdown", () => {', self.html)


if __name__ == "__main__":
    unittest.main()
