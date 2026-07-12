import assert from "node:assert/strict";
import test from "node:test";

import worker from "../src/leaderboard.mjs";

test("returns the saved top scores to the Snake GitHub Pages origin", async () => {
  const response = await worker.fetch(
    new Request("https://snake-leaderboard.example.workers.dev/leaderboard", {
      headers: { Origin: "https://eduard-keilmann.github.io" }
    }),
    {
      LEADERBOARD_DB: {
        prepare(sql) {
          assert.match(sql, /FROM leaderboard_entries/);
          return {
            bind() {
              return {
                all: async () => ({
                  results: [{
                    id: "entry-1",
                    name: "Snake",
                    score: 120,
                    created_at: "2026-07-12T10:00:00.000Z"
                  }]
                })
              };
            }
          };
        }
      },
      LEADERBOARD_RATE_LIMIT_SALT: "test-salt"
    }
  );

  assert.equal(response.status, 200);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), "https://eduard-keilmann.github.io");
  assert.deepEqual(await response.json(), {
    entries: [{
      id: "entry-1",
      name: "Snake",
      score: 120,
      createdAt: "2026-07-12T10:00:00.000Z"
    }]
  });
});

test("starts one rate-limited Snake run without storing the visitor IP", async () => {
  const statements = [];
  const database = {
    prepare(sql) {
      return {
        bind(...values) {
          const statement = {
            sql,
            values,
            async first() {
              if (sql.includes("INSERT INTO leaderboard_rate_limits")) {
                return { count: 1 };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            }
          };
          statements.push(statement);
          return statement;
        }
      };
    },
    async batch(batch) {
      statements.push(...batch);
      return [];
    }
  };

  const response = await worker.fetch(
    new Request("https://snake-leaderboard.example.workers.dev/leaderboard", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Origin: "https://eduard-keilmann.github.io",
        "CF-Connecting-IP": "203.0.113.5"
      },
      body: JSON.stringify({ action: "start" })
    }),
    {
      LEADERBOARD_DB: database,
      LEADERBOARD_RATE_LIMIT_SALT: "test-salt"
    }
  );

  assert.equal(response.status, 201);
  assert.match((await response.json()).runId, /^[0-9a-f-]{36}$/);
  assert.doesNotMatch(JSON.stringify(statements), /203\.0\.113\.5/);
  assert.match(
    statements.find(statement => statement.sql.includes("INSERT INTO leaderboard_runs")).sql,
    /expires_at/
  );
});

test("stores one plausible named score and reports its rank", async () => {
  const statements = [];
  const database = {
    prepare(sql) {
      return {
        bind(...values) {
          const statement = {
            sql,
            values,
            async first() {
              if (sql.includes("SELECT started_at FROM leaderboard_runs")) {
                return { started_at: Date.now() - 2_000 };
              }
              if (sql.includes("SELECT id FROM leaderboard_entries")) {
                return { id: values[0] };
              }
              if (sql.includes("SELECT COUNT(*) AS rank")) {
                return { rank: 0 };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            },
            async run() {
              if (sql.includes("DELETE FROM leaderboard_runs")) {
                return { meta: { changes: 1 } };
              }
              throw new Error(`Unexpected write query: ${sql}`);
            }
          };
          statements.push(statement);
          return statement;
        }
      };
    },
    async batch(batch) {
      statements.push(...batch);
      return [];
    }
  };

  const response = await worker.fetch(
    new Request("https://snake-leaderboard.example.workers.dev/leaderboard", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "submit",
        runId: "run-1",
        name: " Snake ",
        score: 120
      })
    }),
    { LEADERBOARD_DB: database, LEADERBOARD_RATE_LIMIT_SALT: "test-salt" }
  );

  assert.equal(response.status, 201);
  assert.deepEqual(await response.json(), { accepted: true, rank: 1 });
  assert.ok(
    statements.some(statement =>
      statement.sql.includes("INSERT INTO leaderboard_entries") && statement.values.includes("Snake")
    )
  );
});

test("rejects a score that could not be reached during its run", async () => {
  const database = {
    prepare(sql) {
      return {
        bind() {
          return {
            async first() {
              if (sql.includes("SELECT started_at FROM leaderboard_runs")) {
                return { started_at: Date.now() - 1_000 };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            },
            async run() {
              if (sql.includes("DELETE FROM leaderboard_runs")) {
                return { meta: { changes: 1 } };
              }
              throw new Error(`Unexpected write query: ${sql}`);
            }
          };
        }
      };
    }
  };

  const response = await worker.fetch(
    new Request("https://snake-leaderboard.example.workers.dev/leaderboard", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "submit",
        runId: "run-1",
        name: "Snake",
        score: 1_000
      })
    }),
    { LEADERBOARD_DB: database, LEADERBOARD_RATE_LIMIT_SALT: "test-salt" }
  );

  assert.equal(response.status, 422);
  assert.deepEqual(await response.json(), { error: "Score is not plausible for this run" });
});
