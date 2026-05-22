## What to build

Add or update regression tests proving tap control is snake-head-relative and illegal reverse taps are ignored. The tests should protect the existing control modes from accidental removal while the tap behavior changes.

## Acceptance criteria

- [x] Tests assert snake head is used for tap direction origin.
- [x] Tests assert fixed screen-center triangle logic is not used.
- [x] Tests assert reverse tap does not change direction.
- [x] Tests assert swipe and D-pad behavior remain present.
- [x] `python -m unittest discover -s tests` passes.
- [x] `ruff check tests` passes.

## Blocked by

- `issues/001-snake-head-relative-tap-direction.md`
