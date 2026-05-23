## What to build

Update project documentation so it matches the current Snake game and test suite. The README should describe the single-file browser game honestly, mention the current regression-test areas, and state the architecture direction without promising a rewrite.

## Acceptance criteria

- [x] README project structure matches the actual files and test suite.
- [x] README mentions controls, sound, high score, restart behavior, and mobile tap/swipe behavior at the same level as current implementation.
- [x] README explains the intended Module strategy: keep the game simple, deepen behavior where it improves Locality and Leverage.
- [x] Documentation avoids stale claims such as only one D-pad regression test existing.

## Blocked by

- `issues/004-record-snake-architecture-context.md`

## Implemented

- Updated `README.md` so it now describes the current single-file game honestly, including tap/swipe controls, sound, restart confirmation flow, high-score storage, architecture direction, and the actual regression-test areas.
- Added `tests/test_readme_notes.py` as a focused documentation regression test for the README promises.
- Pointed the README and regression test back to `CONTEXT.local.md`, which is the existing durable architecture note.
