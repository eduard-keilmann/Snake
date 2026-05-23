## What to build

Route keyboard, D-pad, continuous swipe, and tap controls through one input command Seam so browser event Adapters translate gestures into player intent while restart, running-state, and direction-policy decisions stay local to game behavior.

## Acceptance criteria

- [x] Keyboard, D-pad, swipe, and tap controls still work in browser play.
- [x] A stopped game still starts cleanly when a valid movement control is used.
- [x] Illegal reverse direction remains ignored.
- [x] Restart-confirmation state still blocks direction changes.
- [x] Focused tests cover at least two control modes through the shared command path rather than exact event-handler text.

## Blocked by

- `issues/005-deepen-snake-game-rules-module.md`

## Notes

- Added a tiny inline `inputCommands` seam in `Snake_browser_game.html` with a shared `move` command.
- Added `handleInputCommand(command)` so running-state and direction-policy decisions stay in game behavior instead of browser event adapters.
- Routed keyboard, D-pad, swipe, and tap controls through that shared move-command path.
- Added focused regression coverage in `tests/test_input_command_seam.py` and updated related HTML-structure tests to match the new seam.
