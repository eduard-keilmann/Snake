## What to build

Route keyboard, D-pad, continuous swipe, and tap controls through one input command Seam so browser event Adapters translate gestures into player intent while restart, running-state, and direction-policy decisions stay local to game behavior.

## Acceptance criteria

- [ ] Keyboard, D-pad, swipe, and tap controls still work in browser play.
- [ ] A stopped game still starts cleanly when a valid movement control is used.
- [ ] Illegal reverse direction remains ignored.
- [ ] Restart-confirmation state still blocks direction changes.
- [ ] Focused tests cover at least two control modes through the shared command path rather than exact event-handler text.

## Blocked by

- `issues/005-deepen-snake-game-rules-module.md`
