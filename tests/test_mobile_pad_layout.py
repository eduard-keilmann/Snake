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


if __name__ == "__main__":
    unittest.main()
