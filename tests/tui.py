"""Drive a real ncurses program inside tmux and read back the screen.

The harness launches a compiled example in a detached tmux pane at a fixed
size, sends real keystrokes to it, and captures the rendered screen so tests
can assert on exactly what a user would see in their terminal.

It shells out to the ``tmux`` binary, so it must run somewhere tmux and the
ncurses runtime exist. On Windows that means WSL (see tests/README.md).

Typical use::

    from tui import Tui

    with Tui("bin/02-07_yourname") as t:
        t.wait_for("first name")
        t.type("Grace")
        t.key("Enter")
        t.type("Hopper")
        t.key("Enter")
        t.wait_for("Pleased to meet you, Grace Hopper!")

Nothing here depends on a test framework; the example suite happens to use
``unittest``, but the harness is a plain object you can drive from any script.
"""

from __future__ import annotations

import itertools
import subprocess
import time

# A private tmux server socket keeps these sessions isolated from any tmux the
# developer is already running. -L names a socket under the tmux tmp dir.
_SOCKET = "ncurses-test"

# Monotonically increasing suffix so concurrent/​repeated sessions never collide.
_counter = itertools.count(1)


class TmuxError(RuntimeError):
    """Raised when an underlying tmux command fails."""


class Tui:
    """A single ncurses program running in a controlled tmux pane.

    Args:
        command: path to the binary (and optional args) to run. May be a
            string (split on spaces) or a list of argv tokens.
        cols, rows: the exact terminal size the program sees. ncurses reads
            these as ``COLS`` / ``LINES``, so they make geometry deterministic.
        term: the ``TERM`` value for the pane. ``screen`` (tmux's default) is a
            safe, widely available choice that supports color and ACS glyphs.
        settle: seconds to wait after launch / after each key batch for the
            program to repaint. Prefer :meth:`wait_for` over a long settle.
    """

    def __init__(self, command, *, cols=80, rows=24, term="screen", settle=0.15):
        self.command = command if isinstance(command, list) else command.split()
        self.cols = cols
        self.rows = rows
        self.term = term
        self.settle = settle
        self.session = f"nc{next(_counter)}"
        self._started = False

    # -- lifecycle ---------------------------------------------------------

    def start(self):
        # One compound command so the option is applied before the pane spawns:
        # `set -g default-terminal <term>` auto-starts the server and fixes the
        # TERM that the new pane (and thus ncurses) will inherit, then
        # `new-session` launches the program at the exact size we want.
        self._tmux(
            "set-option", "-g", "default-terminal", self.term, ";",
            "new-session", "-d", "-s", self.session,
            "-x", str(self.cols), "-y", str(self.rows),
            *self.command,
        )
        # remain-on-exit keeps the final frame capturable after the program
        # calls endwin() and exits, so we can assert on end state.
        self._tmux("set-option", "-t", self.session, "remain-on-exit", "on")
        self._started = True
        time.sleep(self.settle)
        return self

    def stop(self):
        if self._started:
            self._tmux("kill-session", "-t", self.session, check=False)
            self._started = False

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()
        return False

    # -- input -------------------------------------------------------------

    def type(self, text):
        """Send literal text, character for character (no key-name parsing)."""
        # -l = literal: a leading '-' or words like "Up" are sent as typed.
        self._tmux("send-keys", "-t", self.session, "-l", text)
        time.sleep(self.settle)
        return self

    def key(self, *keys):
        """Send one or more named keys, e.g. ``Enter``, ``Up``, ``Space``,
        ``C-c`` (Ctrl-C), ``M-x`` (Alt-x), ``BSpace``, ``Tab``."""
        self._tmux("send-keys", "-t", self.session, *keys)
        time.sleep(self.settle)
        return self

    # -- output ------------------------------------------------------------

    def screen(self):
        """The visible screen as a list of right-stripped lines."""
        out = self._capture()
        return [line.rstrip() for line in out.split("\n")]

    def text(self):
        """The whole visible screen as one newline-joined, stripped string."""
        return "\n".join(self.screen()).strip("\n")

    def screen_ansi(self):
        """The screen including SGR escape sequences (color / attributes).

        Use this to assert on color pairs and attributes, e.g. ``\\x1b[33m``
        for a yellow foreground.
        """
        return self._capture(escapes=True)

    def line(self, n):
        """A single right-stripped row (0-indexed)."""
        rows = self.screen()
        return rows[n] if 0 <= n < len(rows) else ""

    # -- synchronization ---------------------------------------------------

    def wait_for(self, substring, timeout=2.0, interval=0.05):
        """Poll the screen until ``substring`` appears. Returns the full text.

        Raises :class:`TimeoutError` (with the last screen) if it never shows.
        This is the robust alternative to sleeping a fixed amount.
        """
        deadline = time.monotonic() + timeout
        last = ""
        while time.monotonic() < deadline:
            last = self.text()
            if substring in last:
                return last
            time.sleep(interval)
        raise TimeoutError(
            f"{substring!r} did not appear within {timeout}s.\n"
            f"--- last screen ---\n{last}\n-------------------"
        )

    def wait_until(self, predicate, timeout=2.0, interval=0.05):
        """Poll until ``predicate()`` is truthy. Returns its value.

        For screens with no distinctive text to wait on (e.g. a drawn border),
        pass a predicate over the captured screen, such as
        ``lambda: len(t.line(0)) == cols``. Raises :class:`TimeoutError` (with
        the last screen) on timeout.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            value = predicate()
            if value:
                return value
            time.sleep(interval)
        raise TimeoutError(
            f"predicate not satisfied within {timeout}s.\n"
            f"--- last screen ---\n{self.text()}\n-------------------"
        )

    def wait_for_exit(self, timeout=2.0, interval=0.05):
        """Block until the program's process exits. Returns True, or raises
        :class:`TimeoutError` if it is still running at the deadline."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.is_running():
                return True
            time.sleep(interval)
        raise TimeoutError(f"program still running after {timeout}s")

    def is_running(self):
        """True while the program's process is alive in its pane."""
        dead = self._tmux(
            "list-panes", "-t", self.session, "-F", "#{pane_dead}",
        ).strip()
        return dead == "0"

    # -- tmux plumbing -----------------------------------------------------

    def _capture(self, escapes=False):
        args = ["capture-pane", "-p", "-t", self.session]
        if escapes:
            args.insert(1, "-e")
        return self._tmux(*args)

    def _tmux(self, *args, check=True):
        proc = subprocess.run(
            ["tmux", "-L", _SOCKET, *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        if check and proc.returncode != 0:
            raise TmuxError(
                f"tmux {' '.join(args)} failed ({proc.returncode}): "
                f"{proc.stderr.strip()}"
            )
        return proc.stdout
