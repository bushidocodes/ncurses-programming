# TUI tests

These tests drive the **actual compiled programs** — not mocks — and assert on
what gets painted to the terminal. Each test launches an example inside a
detached [`tmux`](https://github.com/tmux/tmux) pane at a fixed size, sends real
keystrokes to it, and reads the rendered screen back with `tmux capture-pane`.
That captured text (and, for color tests, its escape sequences) is exactly what
a user would see, so the assertions exercise the real ncurses rendering path.

## Why tmux

ncurses talks to a terminal, so to test it you need a terminal. `tmux` gives us
a *headless, scriptable* one:

- **Deterministic size** — the pane is created with `-x COLS -y ROWS`, so
  `getmaxx`/`getmaxy`, layout math, and wrapping behave identically every run.
- **Real input** — `send-keys` injects genuine keypresses, including named keys
  (`Up`, `Enter`, `Space`, `C-c`), so keypad and `getch` paths are tested.
- **Faithful output** — `capture-pane -p` returns the visible grid; `-e` adds
  SGR escape sequences so color pairs and attributes can be asserted too.
- **No display required** — it runs in CI with no X server or real TTY.

## Requirements

`tmux`, `python3` (3.8+, standard library only — no pip installs), plus the
`gcc` + `libncursesw` toolchain used to build the examples.

On **Windows**, ncurses lives under WSL, so run the tests there:

```bash
wsl -e bash tests/run.sh
```

On **Linux** (and in CI):

```bash
tests/run.sh
# or, equivalently:
make && python3 -m unittest discover -s tests -v
```

`run.sh` checks the toolchain, builds every example via `make`, then runs the
suite.

## Layout

| File | Purpose |
|------|---------|
| [`tui.py`](tui.py) | The harness — a `Tui` class wrapping tmux (launch, `type`, `key`, `screen`, `screen_ansi`, `wait_for`, `wait_until`, `wait_for_exit`). No test-framework dependency. |
| [`test_examples.py`](test_examples.py) | One representative `unittest` case per category of behavior — the curated showcase. |
| [`test_programs.py`](test_programs.py) | Broad coverage across the example programs, grouped by behavior. Its module docstring lists the few programs left uncovered and why. |
| [`run.sh`](run.sh) | Build + run convenience wrapper. |

Between the two files, the suite drives the large majority of the 100 example
programs. The handful that are not asserted on — mouse-event injection,
multi-second fixed sleeps, and ambiguous alternate-character-set glyphs — are
enumerated with reasons at the top of `test_programs.py` rather than skipped
silently.

## Writing a new test

Import the harness and drive a binary. Prefer `wait_for(...)` over fixed sleeps —
it polls the screen until the expected text shows up (or fails with the last
frame attached, which makes debugging easy).

```python
from tui import Tui

with Tui("bin/02-07_yourname", cols=80, rows=24) as t:
    t.wait_for("first name")          # block until the prompt paints
    t.type("Grace")                   # literal keystrokes
    t.key("Enter")                    # a named key
    t.type("Hopper"); t.key("Enter")
    t.wait_for("Pleased to meet you, Grace Hopper!")
```

Patterns covered in `test_examples.py`, each a template to copy:

- **Static output** — assert a line, confirm it waits in `getch`, then exits.
- **Keyboard input** — type text, assert the echoed/greeting screen.
- **Named keys** — send `Up`/`Down`/… and assert the labels.
- **Non-blocking input** — `nodelay` loop that stops on `Space`.
- **Color / attributes** — assert SGR codes from `screen_ansi()`.
- **Geometry** — request a size, assert the reported dimensions.
- **Borders** — assert a full frame at the screen edges.
- **Windows** — reveal subwindows step by step and assert each appears.

## Notes & gotchas

- Tests use a private tmux socket (`-L ncurses-test`) so they never touch a
  tmux session you already have open.
- `remain-on-exit` keeps the final frame capturable after a program calls
  `endwin()`, so you can assert on end state and detect exit via
  `wait_for_exit()`.
- `capture-pane` trims trailing whitespace per line, so `screen()` lines are
  right-stripped. Index columns from a known-width row (e.g. a border) when you
  need exact positions.
- The default `TERM` is `screen` (tmux's default), which supports color and ACS
  line-drawing glyphs. Override per-test via `Tui(..., term="xterm-256color")`.
