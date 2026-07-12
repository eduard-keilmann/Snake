# Schnäcke (pronounce like "snake") Browser Game

A simple retro Snake game implemented as a single HTML file.

## Tech Stack

- HTML for structure
- CSS for styling and responsive layout
- Vanilla JavaScript for game logic, canvas drawing, controls, sound, restart flow, local high-score handling, and optional online highscores
- Cloudflare Worker + D1 for the optional persistent online leaderboard
- Python `unittest` for focused regression tests

## Play

Play the game on GitHub Pages: <https://eduard-keilmann.github.io/Snake/Snake_browser_game.html>

## Run

Open `Snake_browser_game.html` in a web browser.

No build step, server, or dependency install is required.

## Controls

- Desktop: arrow keys or WASD
- Mobile: hold your finger down and swipe continuously anywhere on the page, tap the game field relative to the snake head, or use the on-screen direction buttons
- Space: start, pause, or resume
- Enter: start when the game is not running
- Restart: click once to pause and show confirmation, then confirm to restart or cancel to resume
- Sound: optional retro-style effects for turns, food, pause/start, and game over

## Gameplay

Eat food to increase the score. The snake wraps around screen edges. The game ends when the snake runs into itself.

High score is loaded from browser storage and updated when a run beats it. When the optional Cloudflare service is available, the player can also save a name and score in the online top 100. Same names are allowed repeatedly. Each online entry shows the reached time.

## Optional Online Highscores

The game remains fully playable on GitHub Pages without Cloudflare. If the Worker cannot be reached, the `HIGHSCORES` button stays hidden and the existing local high score continues to work unchanged.

The Worker in `src/leaderboard.mjs` stores the online top 100 in Cloudflare D1. It accepts only one score per short-lived run ticket, validates names and Snake's ten-point score increments, rate-limits run starts, and rejects scores that could not fit into the measured game duration. This discourages simple browser-side score changes but cannot make a public, client-run game cheat-proof.

### First deployment

From this repository's root:

```sh
npx wrangler@latest login
npx wrangler@latest d1 create snake-leaderboard
```

Copy the `database_id` printed by the second command into `wrangler.toml`, replacing the all-zero placeholder. Then create the tables, set the private rate-limit salt, and deploy:

```sh
npx wrangler@latest d1 migrations apply snake-leaderboard --remote
npx wrangler@latest secret put LEADERBOARD_RATE_LIMIT_SALT
npx wrangler@latest deploy
```

`wrangler deploy` prints a URL like `https://snake-leaderboard.YOUR_SUBDOMAIN.workers.dev`. Copy that exact URL into `LEADERBOARD_API_URL` in `Snake_browser_game.html`, replacing its placeholder, then publish the changed HTML to GitHub Pages.

`LEADERBOARD_RATE_LIMIT_SALT` must be a private random value and must never be committed. For example, generate one locally with `openssl rand -hex 32`, then paste it when Wrangler asks for the secret.

### Local test with D1

```sh
cp .dev.vars.example .dev.vars
# Replace the value in .dev.vars with a private random value.
npx wrangler@latest d1 migrations apply snake-leaderboard --local
npx wrangler@latest dev
```

In a second terminal from the same directory:

```sh
python3 -m http.server 8080
```

Open exactly <http://localhost:8080/Snake_browser_game.html>. The HTML automatically uses `http://localhost:8787/leaderboard` there.

## Architecture Direction

Keep the game simple as a single-file browser game, but deepen behavior only where it improves Locality and Leverage.

Current architecture intent is recorded in `CONTEXT.local.md`.

Today that means:

- keep `Snake_browser_game.html` as the playable delivery unit
- deepen game rules where behavior benefits from direct tests
- route controls through a shared input-command seam instead of spreading direction policy across event handlers
- keep browser-only effects such as sound, storage, vibration, overlays, and timers behind small browser adapters

## Project Structure

- `Snake_browser_game.html`: complete game, including HTML, CSS, and JavaScript
- `src/leaderboard.mjs`: optional Cloudflare Worker API for the online leaderboard
- `migrations/0001_create_leaderboard.sql`: persistent D1 schema for scores, run tickets, and rate limits
- `wrangler.toml`: Worker and D1 binding configuration
- `CONTEXT.local.md`: short architecture note for current Snake structure and vocabulary
- `tests/test_snake_game_rules.py`: focused game-rules behavior regressions
- `tests/test_input_command_seam.py`: shared move-command behavior regressions for keyboard, D-pad, swipe, and tap inputs
- `tests/test_browser_effect_adapters.py`: browser effect adapter regressions for storage, sound, vibration, overlays, and timers
- `tests/test_game_over_restart_behavior.py`: restart and game-over flow regressions
- `tests/test_high_score_storage.py`: high-score display and browser storage regressions
- `tests/test_sound_feedback.py`: retro sound feedback regressions
- `tests/test_mobile_pad_layout.py`: mobile layout and control-surface regressions
- `tests/test_online_leaderboard.py`: online leaderboard UI and gameplay-flow regressions
- `tests/test_leaderboard_schema.py`: D1-compatible schema constraints
- `tests/leaderboard_worker.test.mjs`: Worker API contract and score-plausibility regressions
- `tests/test_architecture_context_note.py`: architecture note regression for `CONTEXT.local.md`
- `tests/test_readme_notes.py`: README regression for current documentation promises
