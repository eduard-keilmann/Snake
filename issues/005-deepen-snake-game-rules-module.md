## What to build

Deepen the Snake game rules Module so movement, wrapping, food eating, scoring, self-collision, and speed changes can be reasoned about as one behavior path without needing to understand rendering, audio, storage, or browser events.

## Acceptance criteria

- [x] A complete play tick can be verified through the game rules Module.
- [x] Snake movement, wraparound, food consumption, score changes, self-collision, and speed changes remain unchanged for players.
- [x] Rendering, sound, vibration, storage, and DOM overlay behavior remain observable in normal browser play.
- [x] Focused regression tests cover at least one movement path, one food path, and one game-over path through the new test surface.
- [x] No new runtime dependency is added.

## Blocked by

- `issues/004-record-snake-architecture-context.md`

## Notes

- Kept the runtime as a single-file browser game by inlining a small `gameRules` seam inside `Snake_browser_game.html`.
- `Snake_browser_game.html` now delegates reset-state creation, food placement, and full tick resolution to that inline rules module while keeping rendering, audio, storage, timers, vibration, and overlays in the browser layer.
- Added focused regression coverage in `tests/test_snake_game_rules.py` for movement, wraparound, food, and game-over paths.
