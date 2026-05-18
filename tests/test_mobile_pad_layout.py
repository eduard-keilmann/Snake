from pathlib import Path
import unittest


class MobilePadLayoutTest(unittest.TestCase):
    def setUp(self):
        self.html = Path("Snake_browser_game.html").read_text(encoding="utf-8")

    def test_d_pad_controls_are_compact_for_mobile_play(self):
        self.assertIn("grid-template-columns: 52px 52px 52px;", self.html)
        self.assertIn("grid-template-rows: 46px 46px 46px;", self.html)
        self.assertIn("gap: 2px;", self.html)
        self.assertIn("transform: translateY(8px);", self.html)
        self.assertIn("transform: translateY(-8px);", self.html)


if __name__ == "__main__":
    unittest.main()
