from pathlib import Path
import unittest


class MobilePadLayoutTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_d_pad_controls_are_compact_for_mobile_play(self):
        self.assertIn("position: relative;", self.html)
        self.assertIn("width: 124px;", self.html)
        self.assertIn("height: 124px;", self.html)
        self.assertIn("width: 56px;", self.html)
        self.assertIn("height: 56px;", self.html)
        self.assertIn("left: 34px;", self.html)
        self.assertIn("top: 0;", self.html)
        self.assertIn("top: 68px;", self.html)


if __name__ == "__main__":
    unittest.main()
