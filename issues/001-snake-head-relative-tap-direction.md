## What to build

Change game field tap control so the intended direction is computed from the snake head position, not from fixed screen-center triangle zones. A tap should mean "turn toward the tapped point relative to the snake head." If the intended direction would reverse into the snake body, ignore the tap rather than choosing an automatic fallback.

## Acceptance criteria

- [x] Tap point is converted into game/canvas coordinates.
- [x] Snake head center is used as direction origin.
- [x] Dominant axis decides intended direction.
- [x] Same-direction tap causes no behavioral regression.
- [x] Reverse-direction tap is ignored, not auto-fallbacked.
- [x] Existing D-pad, continuous swipe, keyboard, sound, restart, and no-scroll behavior remain unchanged.

## Blocked by

None - can start immediately
