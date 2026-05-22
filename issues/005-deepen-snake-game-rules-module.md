## What to build

Deepen the Snake game rules Module so movement, wrapping, food eating, scoring, self-collision, and speed changes can be reasoned about as one behavior path without needing to understand rendering, audio, storage, or browser events.

## Acceptance criteria

- [ ] A complete play tick can be verified through the game rules Module.
- [ ] Snake movement, wraparound, food consumption, score changes, self-collision, and speed changes remain unchanged for players.
- [ ] Rendering, sound, vibration, storage, and DOM overlay behavior remain observable in normal browser play.
- [ ] Focused regression tests cover at least one movement path, one food path, and one game-over path through the new test surface.
- [ ] No new runtime dependency is added.

## Blocked by

- `issues/004-record-snake-architecture-context.md`
