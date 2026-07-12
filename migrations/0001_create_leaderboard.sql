CREATE TABLE leaderboard_entries (
  id TEXT PRIMARY KEY NOT NULL,
  name TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 20),
  score INTEGER NOT NULL CHECK (score >= 0 AND score % 10 = 0),
  created_at TEXT NOT NULL
);

CREATE INDEX leaderboard_entries_rank
  ON leaderboard_entries (score DESC, created_at ASC, id ASC);

CREATE TABLE leaderboard_runs (
  id TEXT PRIMARY KEY NOT NULL,
  started_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);

CREATE INDEX leaderboard_runs_expiry ON leaderboard_runs (expires_at);

CREATE TABLE leaderboard_rate_limits (
  rate_key TEXT PRIMARY KEY NOT NULL,
  count INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);

CREATE INDEX leaderboard_rate_limits_expiry ON leaderboard_rate_limits (expires_at);
