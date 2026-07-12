from __future__ import annotations

from pathlib import Path
import sqlite3
import unittest


class LeaderboardSchemaTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        migration = Path("migrations/0001_create_leaderboard.sql").read_text(encoding="utf-8")
        self.connection.executescript(migration)

    def tearDown(self):
        self.connection.close()

    def test_keeps_duplicate_names_but_rejects_scores_that_snake_cannot_produce(self):
        self.connection.execute(
            "INSERT INTO leaderboard_entries (id, name, score, created_at) VALUES (?, ?, ?, ?)",
            ("first", "Snake", 120, "2026-07-12T10:00:00.000Z"),
        )
        self.connection.execute(
            "INSERT INTO leaderboard_entries (id, name, score, created_at) VALUES (?, ?, ?, ?)",
            ("second", "Snake", 240, "2026-07-12T10:01:00.000Z"),
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO leaderboard_entries (id, name, score, created_at) VALUES (?, ?, ?, ?)",
                ("invalid", "Snake", 125, "2026-07-12T10:02:00.000Z"),
            )

        rows = self.connection.execute(
            "SELECT name, score FROM leaderboard_entries ORDER BY score DESC"
        ).fetchall()
        self.assertEqual(rows, [("Snake", 240), ("Snake", 120)])


if __name__ == "__main__":
    unittest.main()
