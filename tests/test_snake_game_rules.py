from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


def load_rules_module_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"const gameRules = \(\(\) => \{.*?\n    \}\)\(\);",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find inline gameRules module in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def run_rules_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        ["node", "-e", f"{load_rules_module_script()}\n{script}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class SnakeGameRulesTest(unittest.TestCase):
    def test_tick_moves_snake_forward_without_food_or_game_over(self):
        result = run_rules_script(
            textwrap.dedent(
                """
                const result = gameRules.tick({
                  snake: [
                    { x: 10, y: 10 },
                    { x: 9, y: 10 },
                    { x: 8, y: 10 }
                  ],
                  direction: { x: 1, y: 0 },
                  food: { x: 2, y: 2 },
                  score: 0,
                  speed: 180
                }, 20);

                console.log(JSON.stringify(result));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "snake": [
                    {"x": 11, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 9, "y": 10},
                ],
                "food": {"x": 2, "y": 2},
                "score": 0,
                "speed": 180,
                "ateFood": False,
                "gameOver": False,
            },
        )

    def test_tick_grows_snake_updates_score_and_replaces_food(self):
        result = run_rules_script(
            textwrap.dedent(
                """
                const result = gameRules.tick({
                  snake: [
                    { x: 10, y: 10 },
                    { x: 9, y: 10 },
                    { x: 8, y: 10 }
                  ],
                  direction: { x: 1, y: 0 },
                  food: { x: 11, y: 10 },
                  score: 0,
                  speed: 180
                }, 20, () => ({ x: 4, y: 6 }));

                console.log(JSON.stringify(result));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "snake": [
                    {"x": 11, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 9, "y": 10},
                    {"x": 8, "y": 10},
                ],
                "food": {"x": 4, "y": 6},
                "score": 10,
                "speed": 179,
                "ateFood": True,
                "gameOver": False,
            },
        )

    def test_tick_wraps_head_across_left_edge(self):
        result = run_rules_script(
            textwrap.dedent(
                """
                const result = gameRules.tick({
                  snake: [
                    { x: 0, y: 5 },
                    { x: 1, y: 5 },
                    { x: 2, y: 5 }
                  ],
                  direction: { x: -1, y: 0 },
                  food: { x: 9, y: 9 },
                  score: 0,
                  speed: 180
                }, 20);

                console.log(JSON.stringify(result));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "snake": [
                    {"x": 19, "y": 5},
                    {"x": 0, "y": 5},
                    {"x": 1, "y": 5},
                ],
                "food": {"x": 9, "y": 9},
                "score": 0,
                "speed": 180,
                "ateFood": False,
                "gameOver": False,
            },
        )

    def test_tick_reports_game_over_without_mutating_snake_on_self_collision(self):
        result = run_rules_script(
            textwrap.dedent(
                """
                const result = gameRules.tick({
                  snake: [
                    { x: 10, y: 10 },
                    { x: 11, y: 10 },
                    { x: 11, y: 11 },
                    { x: 10, y: 11 }
                  ],
                  direction: { x: 1, y: 0 },
                  food: { x: 2, y: 2 },
                  score: 30,
                  speed: 170
                }, 20);

                console.log(JSON.stringify(result));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "snake": [
                    {"x": 10, "y": 10},
                    {"x": 11, "y": 10},
                    {"x": 11, "y": 11},
                    {"x": 10, "y": 11},
                ],
                "food": {"x": 2, "y": 2},
                "score": 30,
                "speed": 170,
                "ateFood": False,
                "gameOver": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
