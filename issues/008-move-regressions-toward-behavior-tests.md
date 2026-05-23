## What to build

Move high-risk regressions away from substring assertions and toward behavior tests at the chosen game and input seams, while keeping cheap text checks only where they protect static layout or documentation.

## Acceptance criteria

- [x] Existing player-visible behavior covered by current tests remains protected.
- [x] Tests no longer require exact internal formatting for game-over restart, accepted turns, reverse-turn rejection, or high-score promotion.
- [x] Static layout checks remain small and readable.
- [x] The test command used in the repo passes with focused output.
- [x] Tests fail if real Snake behavior is removed, not only if text is renamed.

## Blocked by

- `issues/005-deepen-snake-game-rules-module.md`
- `issues/006-route-controls-through-input-command-seam.md`
