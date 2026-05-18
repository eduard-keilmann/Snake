# Snake Browser Game

A simple Nokia-style Snake game implemented as a single HTML file.

## Tech Stack

- HTML for structure
- CSS for styling and responsive layout
- Vanilla JavaScript for game logic, canvas drawing, keyboard controls, touch controls, pause, restart, and scoring
- Python `unittest` for the small mobile D-pad layout regression test

## Play

Play the game on GitHub Pages: <https://eduard-keilmann.github.io/Snake/Snake_browser_game.html>

## Run

Open `Snake_browser_game.html` in a web browser.

No build step, server, or dependency install is required.

## Controls

- Desktop: arrow keys or WASD
- Mobile: swipe on the game area or use the on-screen direction buttons
- Space: start, pause, or resume
- Enter: start when the game is not running

## Gameplay

Eat food to increase the score. The snake wraps around screen edges. The game ends when the snake runs into itself.

## Project Structure

- `Snake_browser_game.html`: complete game, including HTML, CSS, and JavaScript
- `tests/test_mobile_pad_layout.py`: regression test for the mobile D-pad layout
