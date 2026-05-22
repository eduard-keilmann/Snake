## What to build

Localize browser effects so sound, high-score storage, vibration, timer scheduling, and overlay updates are Adapter-like implementations behind small seams, while game transitions decide what happened without carrying browser quirks.

## Acceptance criteria

- [ ] Sound still plays for start, turn, food, pause, and game over when enabled.
- [ ] Sound toggle and first-gesture audio unlock still work on supported browsers.
- [ ] High score still loads, promotes, saves, and tolerates blocked storage.
- [ ] Vibration remains optional and does not break unsupported browsers.
- [ ] Focused tests prove blocked storage and disabled or unavailable audio do not break core gameplay.

## Blocked by

- `issues/005-deepen-snake-game-rules-module.md`
