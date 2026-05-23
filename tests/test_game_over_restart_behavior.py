from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


def load_start_game_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"function startGame\(\) \{.*?\n    \}",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find startGame in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def run_start_game_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        ["node", "-e", f"{load_start_game_script()}\n{script}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class GameOverRestartBehaviorTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_starting_after_game_over_resets_stale_game_state_before_resuming(self):
        result = run_start_game_script(
            textwrap.dedent(
                """
                let isGameOver = true;
                let isRunning = false;
                let isPaused = true;
                let speed = 160;
                const calls = [];
                const pauseButton = { textContent: "RESUME" };
                const gameTimer = {
                  clear() {
                    calls.push("clear");
                  },
                  start(value) {
                    calls.push(`start:${value}`);
                  }
                };
                const soundEffects = {
                  play(name) {
                    calls.push(`sound:${name}`);
                  }
                };
                const overlayEffects = {
                  hide() {
                    calls.push("hide");
                  }
                };

                function resetGame() {
                  calls.push("reset");
                  isGameOver = false;
                  isPaused = false;
                }

                function resetRestartConfirmation() {
                  calls.push("resetRestartConfirmation");
                }

                startGame();

                console.log(JSON.stringify({
                  calls,
                  isGameOver,
                  isRunning,
                  isPaused,
                  pauseLabel: pauseButton.textContent
                }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "calls": [
                    "reset",
                    "clear",
                    "sound:start",
                    "resetRestartConfirmation",
                    "hide",
                    "start:160",
                ],
                "isGameOver": False,
                "isRunning": True,
                "isPaused": False,
                "pauseLabel": "PAUSE",
            },
        )

    def test_mobile_direction_buttons_and_swipes_share_move_command_path(self):
        self.assertIn(
            "handleInputCommand(inputCommands.move(button.dataset.direction));",
            self.html,
        )
        self.assertIn(
            "return handleInputCommand(inputCommands.move(newDirection));",
            self.html,
        )


if __name__ == "__main__":
    unittest.main()
