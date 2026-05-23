## What to build

Localize browser effects so sound, high-score storage, vibration, timer scheduling, and overlay updates are Adapter-like implementations behind small seams, while game transitions decide what happened without carrying browser quirks.

## Acceptance criteria

- [x] Sound still plays for start, turn, food, pause, and game over when enabled.
- [x] Sound toggle and first-gesture audio unlock still work on supported browsers.
- [x] High score still loads, promotes, saves, and tolerates blocked storage.
- [x] Vibration remains optional and does not break unsupported browsers.
- [x] Focused tests prove blocked storage and disabled or unavailable audio do not break core gameplay.

## Blocked by

- `issues/005-deepen-snake-game-rules-module.md`

## Notes

- Added a small inline `browserEffects` seam in `Snake_browser_game.html`.
- Localized browser-only sound, storage, vibration, overlay, and timer work behind adapter-like factories while keeping game-state decisions in the existing game flow.
- Replaced direct `localStorage`, `navigator.vibrate`, overlay DOM updates, audio wiring, and interval scheduling calls in gameplay code with `storage`, `vibration`, `overlayEffects`, `soundEffects`, and `gameTimer`.
- Added focused regression coverage in `tests/test_browser_effect_adapters.py` for blocked storage and disabled or unavailable audio behavior.
- Updated existing HTML-structure regressions to reflect the new browser-effect seam.
