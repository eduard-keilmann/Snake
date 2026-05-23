# Schnäcke (pronounce like "snake") Browser Game

A simple retro Snake game implemented as a single HTML file.

## Tech Stack

- HTML for structure
- CSS for styling and responsive layout
- Vanilla JavaScript for game logic, canvas drawing, controls, sound, restart flow, high-score handling, and small inline behavior seams
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

High score is loaded from browser storage and updated when a run beats it.

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
- `CONTEXT.local.md`: short architecture note for current Snake structure and vocabulary
- `tests/test_snake_game_rules.py`: focused game-rules behavior regressions
- `tests/test_input_command_seam.py`: shared move-command behavior regressions for keyboard, D-pad, swipe, and tap inputs
- `tests/test_browser_effect_adapters.py`: browser effect adapter regressions for storage, sound, vibration, overlays, and timers
- `tests/test_game_over_restart_behavior.py`: restart and game-over flow regressions
- `tests/test_high_score_storage.py`: high-score display and browser storage regressions
- `tests/test_sound_feedback.py`: retro sound feedback regressions
- `tests/test_mobile_pad_layout.py`: mobile layout and control-surface regressions
- `tests/test_architecture_context_note.py`: architecture note regression for `CONTEXT.local.md`
- `tests/test_readme_notes.py`: README regression for current documentation promises
