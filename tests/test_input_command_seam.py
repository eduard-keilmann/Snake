from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


def load_input_command_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"const inputCommands = \(\(\) => \{.*?\n    \}\)\(\);",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find inline inputCommands module in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def load_handle_input_command_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"function handleInputCommand\(command\) \{.*?\n    \}",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find handleInputCommand in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def load_direction_runtime_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"const directions = \{.*?\n    let snake;",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find directions runtime setup in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0).removesuffix("\n    let snake;")


def load_set_direction_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"function setDirection\(newDirection\) \{.*?\n    \}",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find setDirection in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def run_input_command_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        [
            "node",
            "-e",
            f"{load_input_command_script()}\n{load_handle_input_command_script()}\n{script}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def run_direction_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        [
            "node",
            "-e",
            f"{load_direction_runtime_script()}\n{load_set_direction_script()}\n{script}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class InputCommandSeamTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_keyboard_button_and_touch_controls_share_move_command_path(self):
        self.assertIn('handleInputCommand(inputCommands.move("up"));', self.html)
        self.assertIn("handleInputCommand(inputCommands.move(button.dataset.direction));", self.html)
        self.assertIn("handleInputCommand(inputCommands.move(newDirection));", self.html)

    def test_move_command_restarts_stopped_game_before_turning(self):
        result = run_input_command_script(
            textwrap.dedent(
                """
                let isRunning = false;
                let restartConfirmationPending = false;
                const calls = [];

                function restartGame() {
                  calls.push("restart");
                  isRunning = true;
                }

                function pauseGame() {
                  calls.push("pause");
                }

                function setDirection(direction) {
                  calls.push(`turn:${direction}`);
                  return true;
                }

                const accepted = handleInputCommand(inputCommands.move("left"));

                console.log(JSON.stringify({ accepted, calls, isRunning }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "accepted": True,
                "calls": ["restart", "turn:left"],
                "isRunning": True,
            },
        )

    def test_move_command_keeps_restart_confirmation_block_in_local_game_logic(self):
        result = run_input_command_script(
            textwrap.dedent(
                """
                let isRunning = true;
                let restartConfirmationPending = true;
                const calls = [];

                function restartGame() {
                  calls.push("restart");
                }

                function pauseGame() {
                  calls.push("pause");
                }

                function setDirection(direction) {
                  calls.push(`turn:${direction}`);
                  return false;
                }

                const accepted = handleInputCommand(inputCommands.move("right"));

                console.log(JSON.stringify({ accepted, calls, isRunning }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "accepted": False,
                "calls": ["turn:right"],
                "isRunning": True,
            },
        )

    def test_turn_command_accepts_non_reverse_direction_once(self):
        result = run_direction_script(
            textwrap.dedent(
                """
                let direction = directions.right;
                let nextDirection = directions.right;
                let restartConfirmationPending = false;
                const calls = [];
                const soundEffects = {
                  play(name) {
                    calls.push(name);
                  }
                };

                const accepted = setDirection("up");

                console.log(JSON.stringify({
                  accepted,
                  nextDirection,
                  calls
                }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "accepted": True,
                "nextDirection": {"x": 0, "y": -1},
                "calls": ["turn"],
            },
        )

    def test_turn_command_rejects_reverse_direction_without_feedback(self):
        result = run_direction_script(
            textwrap.dedent(
                """
                let direction = directions.right;
                let nextDirection = directions.right;
                let restartConfirmationPending = false;
                const calls = [];
                const soundEffects = {
                  play(name) {
                    calls.push(name);
                  }
                };

                const accepted = setDirection("left");

                console.log(JSON.stringify({
                  accepted,
                  nextDirection,
                  calls
                }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "accepted": False,
                "nextDirection": {"x": 1, "y": 0},
                "calls": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
