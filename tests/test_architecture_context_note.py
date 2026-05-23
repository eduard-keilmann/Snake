from pathlib import Path
import unittest


class ArchitectureContextNoteTest(unittest.TestCase):
    def test_context_note_records_current_snake_architecture_intent(self):
        note = Path("CONTEXT.local.md").read_text(encoding="utf-8")
        note_lower = note.lower()

        self.assertIn("Snake", note)
        self.assertIn("game rules", note)
        self.assertIn("controls", note)
        self.assertIn("browser effects", note)
        self.assertIn("tests", note)
        self.assertIn("single-file browser game is acceptable for now", note)
        self.assertIn(
            "new seams should be added only where they increase locality or leverage",
            note_lower,
        )
        self.assertIn("No existing ADR currently governs this area", note)
        self.assertIn("the current goal is not a rewrite", note_lower)
        self.assertIn("avoid prescribing a large dependency change", note_lower)


if __name__ == "__main__":
    unittest.main()
