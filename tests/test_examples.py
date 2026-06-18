"""End-to-end TUI tests: each one launches a real compiled example, drives it
with real keystrokes, and asserts on the rendered screen.

Run with:  python3 -m unittest discover -s tests   (inside WSL)
or simply: tests/run.sh

The cases are intentionally representative rather than exhaustive — one per
category of ncurses behavior — so the file doubles as a worked example of how
to test each kind of program. Add more by copying the closest pattern.
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from tui import Tui  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(REPO, "bin")


def setUpModule():
    """Build every example once before the suite runs."""
    subprocess.run(["make"], cwd=REPO, check=True)


def example(name):
    """Absolute path to a built example binary."""
    return os.path.join(BIN, name)


class StaticOutput(unittest.TestCase):
    """A program that just prints and waits for a key."""

    def test_goodbye_prints_message(self):
        with Tui(example("01-01_goodbye")) as t:
            self.assertEqual(t.line(0), "Goodbye, cruel world!")
            # It is parked in getch(), so the process should still be alive.
            self.assertTrue(t.is_running())
            t.key("Enter")
            self.assertTrue(t.wait_for_exit())


class KeyboardInput(unittest.TestCase):
    """Typed text is read back and echoed into the rendered screen."""

    def test_yourname_echoes_and_greets(self):
        with Tui(example("02-07_yourname")) as t:
            t.wait_for("What is your first name?")
            t.type("Grace")
            t.key("Enter")
            t.wait_for("What is your last name?")
            t.type("Hopper")
            t.key("Enter")
            t.wait_for("Pleased to meet you, Grace Hopper!")


class NamedKeys(unittest.TestCase):
    """Arrow keys arrive as KEY_* and the program labels each one."""

    def test_arrowkeys_reports_each_direction(self):
        with Tui(example("08-06_arrowkeys")) as t:
            t.key("Down", "Up", "Left", "Right")
            screen = t.wait_for("Right")
            lines = [ln for ln in screen.splitlines() if ln]
            self.assertEqual(lines[:4], ["Down", "Up", "Left", "Right"])
            # The loop exits on Enter ('\n').
            t.key("Enter")
            self.assertTrue(t.wait_for_exit())


class NonBlockingInput(unittest.TestCase):
    """nodelay() counter keeps running until the spacebar stops it."""

    def test_keywait2_counts_then_stops_on_space(self):
        with Tui(example("08-03_keywait2")) as t:
            t.wait_for("Press any key to begin")
            t.key("a")  # any key starts the non-blocking loop
            t.wait_for("Press any key to start the loop!")
            self.assertTrue(t.is_running())
            t.key("Space")
            self.assertTrue(t.wait_for_exit())


class ColorAndAttributes(unittest.TestCase):
    """Color pairs surface as SGR escape sequences in the capture."""

    def test_yellowred_emits_color_pair(self):
        with Tui(example("03-04_yellowred")) as t:
            t.wait_for("Colored text")
            ansi = t.screen_ansi()
            # init_pair(1, COLOR_YELLOW, COLOR_RED): fg 33, bg 41.
            self.assertIn("\x1b[33m", ansi)  # yellow foreground
            self.assertIn("\x1b[41m", ansi)  # red background
            # Plain text assertions still work alongside color ones.
            self.assertEqual(t.line(0), "Normal Text")
            self.assertEqual(t.line(2), "Back to normal.")


class Geometry(unittest.TestCase):
    """The pane size we request is exactly the size ncurses reports."""

    def test_screensize_matches_requested_dimensions(self):
        with Tui(example("05-01_screensize"), cols=100, rows=30) as t:
            self.assertEqual(t.line(0), "Window is 30 rows by 100 columns")

    def test_screensize_default_80x24(self):
        with Tui(example("05-01_screensize")) as t:
            self.assertEqual(t.line(0), "Window is 24 rows by 80 columns")


class Borders(unittest.TestCase):
    """box() draws a full, closed frame around the screen edges."""

    def test_box_frames_the_screen(self):
        cols, rows = 80, 24
        with Tui(example("00-01_box"), cols=cols, rows=rows) as t:
            # No text to wait on — wait until the border has actually painted.
            t.wait_until(lambda: len(t.line(0)) == cols)
            screen = t.screen()
            top, bottom = screen[0], screen[rows - 1]
            # Top and bottom rows span the full width with no gaps.
            self.assertEqual(len(top), cols)
            self.assertEqual(len(bottom), cols)
            self.assertNotIn(" ", top)
            self.assertNotIn(" ", bottom)
            # Horizontal runs are the '*' we passed to box().
            self.assertEqual(top[1:-1], "*" * (cols - 2))
            # Interior rows have a vertical border on both edges, blank between.
            mid = screen[rows // 2]
            self.assertEqual(mid[0], "*")
            self.assertEqual(mid[cols - 1], "*")
            self.assertEqual(mid[1:-1].strip(), "")


class Windows(unittest.TestCase):
    """A multi-window program revealed one wrefresh() at a time."""

    def test_quad_reveals_windows_in_sequence(self):
        with Tui(example("09-06_quad")) as t:
            # stdscr is drawn first and prompts before any subwindow shows.
            t.wait_for("This is the standard screen")
            self.assertNotIn("first window", t.text())
            t.key("Enter")
            t.wait_for("This is a the first window")
            t.key("Enter")
            t.wait_for("This is a the second window")
            # First window is still on screen after the second appears.
            self.assertIn("This is a the first window", t.text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
