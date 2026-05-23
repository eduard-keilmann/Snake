from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


def load_browser_effects_script() -> str:
    html = Path("Snake_browser_game.html").read_text(encoding="utf-8")
    match = re.search(
        r"const browserEffects = \(\(\) => \{.*?\n    \}\)\(\);",
        html,
        re.DOTALL,
    )
    if not match:
        msg = "Could not find inline browserEffects module in Snake_browser_game.html"
        raise AssertionError(msg)
    return match.group(0)


def run_browser_effects_script(script: str) -> dict[str, object]:
    completed = subprocess.run(
        ["node", "-e", f"{load_browser_effects_script()}\n{script}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class BrowserEffectAdaptersTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_runtime_routes_browser_work_through_effect_adapters(self):
        self.assertIn("const browserEffects = (() => {", self.html)
        self.assertIn("const storage = browserEffects.createStorage(window.localStorage);", self.html)
        self.assertIn("const soundEffects = browserEffects.createSoundEffects({", self.html)
        self.assertIn("const vibration = browserEffects.createVibration({", self.html)
        self.assertIn("const overlayEffects = browserEffects.createOverlay({", self.html)
        self.assertIn("const gameTimer = browserEffects.createTimer(gameLoop);", self.html)
        self.assertIn("highScore = storage.loadNumber(highScoreStorageKey);", self.html)
        self.assertIn("storage.saveNumber(highScoreStorageKey, highScore);", self.html)
        self.assertIn('soundEffects.play("food");', self.html)
        self.assertIn("gameTimer.start(speed);", self.html)
        self.assertIn("overlayEffects.show(", self.html)
        self.assertIn("vibration.run();", self.html)

    def test_blocked_storage_falls_back_to_zero_and_save_is_safe(self):
        result = run_browser_effects_script(
            textwrap.dedent(
                """
                const storage = browserEffects.createStorage({
                  getItem() {
                    throw new Error("blocked");
                  },
                  setItem() {
                    throw new Error("blocked");
                  }
                });

                const loaded = storage.loadNumber("snake");
                const saveResult = storage.saveNumber("snake", 42);

                console.log(JSON.stringify({ loaded, saveResult }));
                """
            )
        )

        self.assertEqual(result, {"loaded": 0, "saveResult": False})

    def test_disabled_or_unavailable_audio_keeps_effect_calls_safe(self):
        result = run_browser_effects_script(
            textwrap.dedent(
                """
                const withoutAudio = browserEffects.createSoundEffects({
                  createAudioContext: null,
                  sounds: {
                    start: [{ frequency: 523, delay: 0, duration: 0.06, volume: 0.08 }]
                  }
                });

                withoutAudio.setEnabled(false);
                withoutAudio.unlock();
                withoutAudio.play("start");

                const withDisabledSound = browserEffects.createSoundEffects({
                  createAudioContext() {
                    return {
                      state: "running",
                      currentTime: 0,
                      destination: {},
                      createBuffer() {
                        throw new Error("should not be called");
                      },
                      createBufferSource() {
                        throw new Error("should not be called");
                      },
                      createOscillator() {
                        throw new Error("should not be called");
                      },
                      createGain() {
                        throw new Error("should not be called");
                      }
                    };
                  },
                  sounds: {
                    start: [{ frequency: 523, delay: 0, duration: 0.06, volume: 0.08 }]
                  }
                });

                withDisabledSound.setEnabled(false);
                withDisabledSound.unlock();
                withDisabledSound.play("start");

                console.log(JSON.stringify({
                  unavailableEnabled: withoutAudio.isEnabled(),
                  disabledEnabled: withDisabledSound.isEnabled()
                }));
                """
            )
        )

        self.assertEqual(
            result,
            {
                "unavailableEnabled": False,
                "disabledEnabled": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
