const GITHUB_PAGES_ORIGIN = "https://eduard-keilmann.github.io";
const RUN_TTL_MS = 4 * 60 * 60 * 1000;

function responseHeaders(request) {
  const headers = new Headers({ "Content-Type": "application/json" });
  const origin = request.headers.get("Origin");

  if (origin === GITHUB_PAGES_ORIGIN || /^http:\/\/localhost:\d+$/.test(origin || "")) {
    headers.set("Access-Control-Allow-Origin", origin);
    headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    headers.set("Access-Control-Allow-Headers", "Content-Type");
    headers.set("Vary", "Origin");
  }

  return headers;
}

function json(request, status, body) {
  return new Response(JSON.stringify(body), { status, headers: responseHeaders(request) });
}

async function rateLimitKey(request, salt, now) {
  const day = new Date(now).toISOString().slice(0, 10);
  const ipAddress = request.headers.get("CF-Connecting-IP") || "";
  const data = new TextEncoder().encode(`${day}:${ipAddress}:${salt}`);
  const digest = await crypto.subtle.digest("SHA-256", data);
  const hash = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
  return `${day}:${hash}`;
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: responseHeaders(request) });
    }

    const url = new URL(request.url);
    if (url.pathname !== "/leaderboard") {
      return json(request, 404, { error: "Not found" });
    }

    if (request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch (_) {
        return json(request, 400, { error: "Invalid request body" });
      }

      if (body?.action === "submit") {
        const name = typeof body.name === "string" ? body.name.trim() : "";
        const score = body.score;

        if (
          typeof body.runId !== "string" ||
          !Number.isSafeInteger(score) ||
          score < 0 ||
          score % 10 !== 0 ||
          !name ||
          Array.from(name).length > 20 ||
          /[\u0000-\u001F\u007F]/.test(name)
        ) {
          return json(request, 400, { error: "Invalid leaderboard score" });
        }

        try {
          const now = Date.now();
          const run = await env.LEADERBOARD_DB.prepare(
            "SELECT started_at FROM leaderboard_runs WHERE id = ? AND expires_at > ?"
          ).bind(body.runId, now).first();

          if (!run) {
            return json(request, 409, { error: "Run ticket is missing or already used" });
          }

          const consumedRun = await env.LEADERBOARD_DB.prepare(
            "DELETE FROM leaderboard_runs WHERE id = ? AND expires_at > ?"
          ).bind(body.runId, now).run();

          if (consumedRun.meta.changes !== 1) {
            return json(request, 409, { error: "Run ticket is missing or already used" });
          }

          const elapsedMs = now - Number(run.started_at);
          if (
            !Number.isFinite(elapsedMs) ||
            elapsedMs < 0 ||
            elapsedMs > RUN_TTL_MS ||
            score > Math.floor(elapsedMs / 100) * 10
          ) {
            return json(request, 422, { error: "Score is not plausible for this run" });
          }

          const entryId = crypto.randomUUID();
          const createdAt = new Date(now).toISOString();
          await env.LEADERBOARD_DB.batch([
            env.LEADERBOARD_DB.prepare(
              "INSERT INTO leaderboard_entries (id, name, score, created_at) VALUES (?, ?, ?, ?)"
            ).bind(entryId, name, score, createdAt),
            env.LEADERBOARD_DB.prepare(
              `DELETE FROM leaderboard_entries
               WHERE id NOT IN (
                 SELECT id FROM leaderboard_entries
                 ORDER BY score DESC, created_at ASC, id ASC
                 LIMIT ?
               )`
            ).bind(100)
          ]);

          const savedEntry = await env.LEADERBOARD_DB.prepare(
            "SELECT id FROM leaderboard_entries WHERE id = ?"
          ).bind(entryId).first();
          if (!savedEntry) {
            return json(request, 200, { accepted: false });
          }

          const rank = await env.LEADERBOARD_DB.prepare(
            `SELECT COUNT(*) AS rank
             FROM leaderboard_entries
             WHERE score > ?
                OR (score = ? AND (created_at < ? OR (created_at = ? AND id < ?)))`
          ).bind(score, score, createdAt, createdAt, entryId).first();

          return json(request, 201, { accepted: true, rank: Number(rank.rank) + 1 });
        } catch (_) {
          return json(request, 503, { error: "Leaderboard unavailable" });
        }
      }

      if (body?.action !== "start") {
        return json(request, 400, { error: "Unknown leaderboard action" });
      }

      if (!env.LEADERBOARD_RATE_LIMIT_SALT) {
        return json(request, 503, { error: "Leaderboard unavailable" });
      }

      try {
        const now = Date.now();
        const expiresAt = new Date(now);
        expiresAt.setUTCHours(24, 0, 0, 0);
        const rate = await env.LEADERBOARD_DB.prepare(
          `INSERT INTO leaderboard_rate_limits (rate_key, count, expires_at)
           VALUES (?, 1, ?)
           ON CONFLICT(rate_key) DO UPDATE SET
             count = CASE WHEN expires_at <= ? THEN 1 ELSE count + 1 END,
             expires_at = CASE WHEN expires_at <= ? THEN excluded.expires_at ELSE expires_at END
           RETURNING count`
        ).bind(
          await rateLimitKey(request, env.LEADERBOARD_RATE_LIMIT_SALT, now),
          expiresAt.getTime(),
          now,
          now
        ).first();

        if (!rate || Number(rate.count) > 30) {
          return json(request, 429, { error: "Too many leaderboard runs today" });
        }

        const runId = crypto.randomUUID();
        await env.LEADERBOARD_DB.batch([
          env.LEADERBOARD_DB.prepare("DELETE FROM leaderboard_runs WHERE expires_at <= ?").bind(now),
          env.LEADERBOARD_DB.prepare("DELETE FROM leaderboard_rate_limits WHERE expires_at <= ?").bind(now),
          env.LEADERBOARD_DB.prepare(
            "INSERT INTO leaderboard_runs (id, started_at, expires_at) VALUES (?, ?, ?)"
          ).bind(runId, now, now + RUN_TTL_MS)
        ]);

        return json(request, 201, { runId });
      } catch (_) {
        return json(request, 503, { error: "Leaderboard unavailable" });
      }
    }

    if (request.method !== "GET") {
      return json(request, 405, { error: "Method not allowed" });
    }

    try {
      const entries = await env.LEADERBOARD_DB.prepare(
        "SELECT id, name, score, created_at FROM leaderboard_entries ORDER BY score DESC, created_at ASC, id ASC LIMIT ?"
      ).bind(100).all();

      return json(request, 200, {
        entries: entries.results.map(entry => ({
          id: entry.id,
          name: entry.name,
          score: entry.score,
          createdAt: entry.created_at
        }))
      });
    } catch (_) {
      return json(request, 503, { error: "Leaderboard unavailable" });
    }
  }
};
