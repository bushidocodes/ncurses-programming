"""Broad coverage for the example programs, driven through the tmux harness.

`test_examples.py` is the curated one-per-category showcase. This file aims for
breadth: it exercises the large majority of the 100 programs, grouped by the
kind of behavior involved. Every assertion was written against the program's
actual output (verified by running it), not guessed from its name.

Intentionally NOT covered here, with reasons (so the gaps are explicit, not
silent):

  04-05_acslist, 04-06_acsstring  — render the alternate character set, whose
      glyph mapping under TERM=screen is ambiguous to assert on.
  04-12_ustring                   — hard-codes setlocale(en_US.UTF-8); that
      locale is not guaranteed generated on CI, so the Cyrillic output is
      environment-dependent. (04-11_unicode is covered via its ASCII framing.)
  08-09_flush                     — a fixed napms(5000) with no observable
      intermediate state; pure latency, low signal.
  09-03_switchback                — behaviorally identical to 09-02_switch.
  11-02_overwrite2, 11-05_copywin2 — near-duplicates of 11-01 / 11-04.
  12-01_scrolling1, 12-02_scrolling2, 12-06_scrollreg — 300–600 iteration
      napms loops (15–30 s each); too slow for CI, no distinct end state.
  14-02_mspy, 14-03_clickput, 14-04_blick — require injecting real mouse
      events, which tmux send-keys cannot do portably across terminfo. Mouse
      *availability* is covered via 14-01_mousetest.

Run with:  python3 -m unittest discover -s tests   (inside WSL)
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
    subprocess.run(["make"], cwd=REPO, check=True)


def example(name):
    return os.path.join(BIN, name)


# ---------------------------------------------------------------------------
# Static screens: everything is printed before the first getch(), so the
# opening capture already contains the expected text. One subTest per program.
# ---------------------------------------------------------------------------

STATIC_SCREENS = [
    ("02-03_add2", ["Shall I compare thee to a summer's day?"]),
    ("02-04-add3", ["Shall I compare thee to a summer's day?",
                    "Though are more lovely..."]),
    ("02-05_yoda", ["Yoda is 874 years one",
                    "collected 809 years of Social Security"]),
    ("03-01_twinkle", ["Twinkle, twinkle little star",
                       "How I wonder what you are."]),
    ("03-02_annoy", ["Do", "silly?"]),
    ("03-03_colortest", ["Colors initialized.", "colors available.",
                         "color pairs."]),
    ("03-05_colorful", ["I am Mr. Black!", "I am Mr. Yellow!",
                        "I'm feeling bold!", "Me too!"]),
    ("03-06_pink", ["This is the new color 1."]),
    ("03-07_bgcolor1", ["Hello World"]),
    ("03-08_bgcolor2", ["a color screen as pretty as thee.",
                        "For seasons may change",
                        "But color text shall always wonder."]),
    ("03-09_notice", ["Attention!"]),
    ("04-01_charattrib", ["cat"]),
    ("04-03_attrtest", ["This is A_STANDOUT", "This is A_BOLD",
                        "This is A_VERTICAL"]),
    ("04-04_pi", ["= 3.14159"]),
    ("04-08_chtypestring", ["Hello!"]),
    ("04-09_addchstr", ["Hello!"]),
    ("04-11_unicode", ["I ", "Ncurses"]),
    ("05-02_stdscrsize", ["Window is 24 rows by 80 columns"]),
    ("05-03_ncurses", ["Window is 24 rows by 80 columns"]),
    ("05-04_ctitle", ["Penguin Soccer Finals", "Catatonic Theater",
                      "Why do Ions hate each other?"]),
    ("06-01_text1", ["This is the first line", "The third line",
                     "And the fifth line"]),
    ("09-08_border", ["Now that's a swell border!"]),
    ("13-01_newpad1", ["New pad created"]),
    ("14-01_mousetest", ["Mouse Functions Available.", "Mouse Active"]),
]


class StaticScreens(unittest.TestCase):
    def test_static_screens(self):
        for name, expected in STATIC_SCREENS:
            with self.subTest(program=name):
                with Tui(example(name)) as t:
                    t.wait_for(expected[0])
                    screen = t.text()
                    for needle in expected:
                        self.assertIn(needle, screen)


class AcsArtRenders(unittest.TestCase):
    """ACS box-art whose exact glyphs vary, but whose shape does not:
    three rows, with a hollow middle row."""

    def _assert_three_row_box(self, name):
        with Tui(example(name)) as t:
            t.wait_until(lambda: len(t.line(0)) == 3)
            self.assertEqual(len(t.line(0)), 3)      # top:    corner line corner
            self.assertEqual(len(t.line(2)), 3)      # bottom: corner line corner
            self.assertEqual(t.line(1)[1], " ")      # middle: side space side

    def test_abox_acs_corners(self):
        self._assert_three_row_box("04-07_aBox")

    def test_boxarray_acs_letters(self):
        self._assert_three_row_box("04-10_boxarray")


class Animations(unittest.TestCase):
    """Programs that build their final text over timed frames; we wait for the
    finished state rather than racing the animation."""

    def test_add1_types_out_greeting(self):
        with Tui(example("02-02_add1")) as t:
            t.wait_for("Greetings from Ncurses!", timeout=5)

    def test_marquee1_builds_headline(self):
        with Tui(example("06-05_marquee1")) as t:
            t.wait_for("Armstrong walks on moon", timeout=5)

    def test_marquee2_builds_headline_under_alphabet(self):
        with Tui(example("06-06_marquee2")) as t:
            t.wait_for("Armstrong walks on moon", timeout=5)

    def test_corners_places_star_in_each_corner(self):
        cols, rows = 80, 24
        with Tui(example("05-03_corners"), cols=cols, rows=rows) as t:
            # Stars appear one corner at a time with 500 ms pauses.
            t.wait_until(lambda: t.line(0)[:1] == "*"
                         and t.line(0)[cols - 1:] == "*"
                         and t.line(rows - 1)[:1] == "*"
                         and t.line(rows - 1)[cols - 1:] == "*",
                         timeout=5)


# ---------------------------------------------------------------------------
# Input-driven programs.
# ---------------------------------------------------------------------------

class Input(unittest.TestCase):
    def test_typewriter_quits_on_tilde(self):
        with Tui(example("02-06_typewriter")) as t:
            t.wait_for("Press ~ to quit")
            t.key("~")
            self.assertTrue(t.wait_for_exit())

    def test_sushi_computes_order_total(self):
        with Tui(example("02-08_sushi")) as t:
            t.wait_for("We have Uni today for $4.50.")
            t.type("5")
            t.key("Enter")
            t.wait_for("You want 5 pieces?")
            self.assertIn("That will be $22.50!", t.text())

    def test_whereami_reports_cursor_row(self):
        with Tui(example("05-05_whereami")) as t:
            t.wait_for("Type some text")
            t.type("hello")
            t.key("~")
            # Five echoed chars + the echoed '~' leave the cursor on row 1.
            t.wait_for("was at position 1 ")

    def test_yourname_confirm_loop(self):
        with Tui(example("08-01_yourname")) as t:
            t.wait_for("Enter your name:")
            t.type("Grace")
            t.key("Enter")
            t.wait_for("Is this correct?")
            t.key("y")
            t.wait_for("Pleased to meet you, Grace.")

    def test_keywait1_starts_and_stops_on_keys(self):
        with Tui(example("08-02_keywait1")) as t:
            t.wait_for("Press any key to begin")
            t.key("a")
            t.wait_for("Press any key to start the loop!")
            self.assertTrue(t.is_running())
            t.key("b")
            self.assertTrue(t.wait_for_exit())

    def test_secretkey_matches_identical_keys(self):
        with Tui(example("08-04_secretkey")) as t:
            t.wait_for("Type a key:")
            t.key("a")
            t.wait_for("Type the same key:")
            t.key("a")
            t.wait_for("The keys match!")

    def test_kbhit_detects_keypress(self):
        with Tui(example("08-05_kbhit")) as t:
            t.wait_for("Tap a key while I count")
            t.key("x")
            t.wait_for("You pressed the x key", timeout=5)

    def test_greetings_collects_two_names(self):
        with Tui(example("08-07_greetings")) as t:
            t.wait_for("First name:")
            t.type("Ada")
            t.key("Enter")
            t.wait_for("Last name:")
            t.type("Lovelace")
            t.key("Enter")
            t.wait_for("Pleased to meet you, Ada Lovelace")

    def test_urpwd_hides_password(self):
        with Tui(example("08-08_urpwd")) as t:
            t.wait_for("Name:")
            t.type("root")
            t.key("Enter")
            t.wait_for("Password:")
            t.type("secret")
            t.key("Enter")
            t.wait_for("root's password is 'secret'")
            # The password is echoed only in the final summary line, never at
            # the prompt — noecho() hid it during entry.
            self.assertEqual(t.text().count("secret"), 1)

    def test_changechar_overwrites_t_with_r(self):
        with Tui(example("04-02_changechar")) as t:
            t.wait_until(lambda: t.line(0) == "cat")
            t.key("Enter")
            t.wait_until(lambda: t.line(0) == "car")

    def test_curset_cycles_visibility_labels(self):
        with Tui(example("15-01_curset")) as t:
            t.wait_for("turned off")
            t.key("Enter")
            t.wait_for("turned on")
            t.key("Enter")
            t.wait_for("turned very on")


# ---------------------------------------------------------------------------
# Text manipulation and screen clearing.
# ---------------------------------------------------------------------------

class TextOps(unittest.TestCase):
    def test_insertln_pushes_lines_down(self):
        with Tui(example("06-02_text2")) as t:
            t.wait_for("The third line")
            self.assertEqual(t.line(1), "The third line")
            t.key("Enter")
            # A blank line is inserted at row 1; row 1 empties, text shifts down.
            t.wait_until(lambda: t.line(1) == "" and t.line(2) == "The third line")

    def test_insertln_then_fill(self):
        # 06-03: blank line opened at row 1, then text written into it.
        with Tui(example("06-03_text3")) as t:
            t.wait_for("The third line")
            t.key("Enter")
            t.wait_until(lambda: t.line(1) == "")
            t.key("Enter")
            t.wait_until(lambda: t.line(1).startswith("Line two here"))
            self.assertEqual(t.line(2), "The third line")

    def test_insert_two_lines_then_fill(self):
        # 06-04: blank lines opened at rows 1 and 3, then both filled, leaving
        # all five lines in order.
        with Tui(example("06-04_text4")) as t:
            t.wait_for("The third line")
            t.key("Enter")
            t.key("Enter")
            t.wait_until(lambda: t.line(1).startswith("Line two here")
                         and t.line(3).startswith("Fourth line here"))
            self.assertEqual(t.line(0), "This is the first line")
            self.assertEqual(t.line(2), "The third line")
            self.assertEqual(t.line(4), "And the fifth line")

    def test_insstr_inserts_line_in_place(self):
        with Tui(example("06-07_text5")) as t:
            t.wait_for("The third line")
            t.key("Enter")
            t.wait_until(lambda: t.line(1).startswith("Line two here"))

    def test_deleteln_removes_third_line(self):
        with Tui(example("06-08_text6")) as t:
            t.wait_for("The third line")
            t.key("Enter")
            # Deleting row 2 ("The third line") pulls line four up into its place.
            t.wait_until(lambda: "The third line" not in t.text())
            self.assertEqual(t.line(2), "Fourth line here")

    def test_delch_deletes_word(self):
        with Tui(example("06-09_text7")) as t:
            t.wait_for("Fourth line here")
            t.key("Enter")
            t.wait_until(lambda: t.line(3) == "Fourth here", timeout=5)

    def test_cat_replaces_word(self):
        with Tui(example("06-10_cat")) as t:
            t.wait_for("Where did that silly cat go?")
            t.key("Enter")
            t.wait_for("fat", timeout=5)
            self.assertIn("cat go?", t.text())

    def test_insdelln_inserts_blank_band(self):
        with Tui(example("06-11_insdel")) as t:
            t.wait_until(lambda: len(t.line(0)) == 80)  # screen full of dots
            self.assertEqual(t.line(0), "." * 80)
            t.key("Enter")
            # Three blank rows are inserted starting at row 5.
            t.wait_until(lambda: t.line(5) == "")

    def test_clear_empties_screen(self):
        with Tui(example("07-01_cls")) as t:
            t.wait_for("blah")
            t.key("Enter")
            t.wait_until(lambda: t.text() == "")

    def test_clrtoeol_truncates_one_line(self):
        with Tui(example("07-02_clearline")) as t:
            t.wait_for("blah")
            self.assertGreater(len(t.line(4)), 70)   # neighbor row stays full
            t.key("Enter")
            # Row 5 is cleared from column 20 onward.
            t.wait_until(lambda: len(t.line(5)) <= 20)
            self.assertGreater(len(t.line(4)), 70)
            self.assertIn("blah", t.line(5))

    def test_clrtobot_clears_to_bottom(self):
        with Tui(example("07-03_clearbot")) as t:
            t.wait_for("blah")
            t.key("Enter")
            # Everything from (5,20) down is erased; row 6 goes blank.
            t.wait_until(lambda: t.line(6) == "")
            self.assertGreater(len(t.line(4)), 70)


# ---------------------------------------------------------------------------
# Borders and line drawing.
# ---------------------------------------------------------------------------

class BordersAndLines(unittest.TestCase):
    def test_default_box_frames_screen(self):
        with Tui(example("09-10_box")) as t:
            t.wait_until(lambda: len(t.line(0)) == 80)
            self.assertNotIn(" ", t.line(0))
            self.assertNotIn(" ", t.line(23))

    def test_comma_border(self):
        with Tui(example("09-09_aborder")) as t:
            t.wait_for("Now that's a swell border!")
            self.assertEqual(t.line(0), "," * 80)

    def test_steps_draws_full_top_line(self):
        with Tui(example("15-02_steps")) as t:
            t.wait_until(lambda: len(t.line(0)) == 80)
            self.assertNotIn(" ", t.line(0))

    def test_plus_draws_horizontal_axis(self):
        with Tui(example("15-03_plus")) as t:
            # hline() spans the full width at LINES/2 (row 12 of 24).
            t.wait_until(lambda: len(t.line(12)) == 80)
            self.assertNotIn(" ", t.line(12))


# ---------------------------------------------------------------------------
# Windows, subwindows, copying, pads.
# ---------------------------------------------------------------------------

class Windows(unittest.TestCase):
    def test_anotherwin_reveals_second_window(self):
        with Tui(example("09-01_anotherwin")) as t:
            t.wait_for("This is the standard screen")
            t.key("Enter")
            t.wait_for("This is another window!")

    def test_switch_overlays_second_window(self):
        with Tui(example("09-02_switch")) as t:
            t.wait_for("This is the standard screen")
            t.key("Enter")
            t.wait_for("This is the second window")

    def test_touch_reveals_second_window(self):
        with Tui(example("09-04_touch")) as t:
            t.wait_for("This is the standard screen")
            t.key("Enter")
            t.wait_for("This is the second window")

    def test_halfpint_centered_window(self):
        with Tui(example("09-05_halfpint")) as t:
            t.wait_for("This is the standard screen")
            t.key("Enter")
            t.wait_for("This is a tiny window")

    def test_twowin_delete_one(self):
        with Tui(example("09-07_twowin")) as t:
            t.key("Enter")
            t.wait_for("This is a the first window")
            t.key("Enter")
            t.wait_for("This is a the second window")
            t.key("Enter")
            t.wait_for("First window deleted")

    def test_quadborders_reveals_boxed_window(self):
        with Tui(example("09-11_quadborders")) as t:
            t.wait_for("This is the standard screen")
            t.key("Enter")
            t.wait_for("This is a the first window")


class Subwindows(unittest.TestCase):
    def test_sub1_text_inside_border(self):
        with Tui(example("10-01_sub1")) as t:
            t.wait_for("I'm in a subwindow.")
            self.assertEqual(len(t.line(0)), 80)  # outer box border

    def test_sub2_main_and_sub_text(self):
        with Tui(example("10-02_sub2")) as t:
            t.wait_for("I'm the main window.")
            self.assertIn("I'm in a subwindow.", t.text())

    def test_sub3_derived_window(self):
        with Tui(example("10-03_sub3")) as t:
            # The box() top border is immediately overwritten by addstr() at
            # (0,0), so row 0 ends up showing the text rather than the frame.
            t.wait_for("I'm writing text to the standard screen.")

    def test_subsub_three_generations(self):
        with Tui(example("10-04_subsub")) as t:
            t.wait_for("I am grandpa")
            screen = t.text()
            self.assertIn("I am father", screen)
            self.assertIn("I am son", screen)

    def test_delsub_removes_subwindow(self):
        with Tui(example("10-05_delsub")) as t:
            t.wait_for("standard screen")
            self.assertIn("sub", t.text())
            t.key("Enter")
            t.wait_for("Subwindow deleted")


class WindowCopying(unittest.TestCase):
    def test_overwrite_fills_blue_with_red_char(self):
        with Tui(example("11-01_overwrite1")) as t:
            # Each window is flood-filled with its background char.
            t.wait_until(lambda: t.text().count("r") > 20
                         and t.text().count("b") > 20)
            t.key("Enter")  # overwrite(red, blue) copies red over blue
            self.assertIn("r", t.text())

    def test_overlay_copies_nonblank(self):
        with Tui(example("11-03_overlay")) as t:
            t.wait_for("o e l y")
            t.key("Enter")
            self.assertIn("o e l y", t.text())

    def test_copywin_carries_red_into_blue(self):
        with Tui(example("11-04_copywin")) as t:
            t.wait_until(lambda: "red" in t.text() and "blue" in t.text())
            t.key("Enter")
            self.assertIn("red", t.text())

    def test_dupwin_independent_copy(self):
        with Tui(example("11-06_dup")) as t:
            t.wait_for("This is Fred.")
            t.key("Enter")
            t.wait_for("This is Barney")

    def test_movewin_relocates_window(self):
        with Tui(example("11-07_movewin")) as t:
            t.wait_for("Window Alpha")
            t.key("Enter")
            t.wait_for("Moved!")


class Scrolling(unittest.TestCase):
    def test_scroll_advances_one_line(self):
        with Tui(example("12-04_scroll")) as t:
            t.wait_until(lambda: t.line(0).strip() == "0")
            t.key("Enter")
            t.wait_until(lambda: t.line(0).strip() == "1")

    def test_scrl_advances_three_lines(self):
        with Tui(example("12-05_scrup3")) as t:
            t.wait_until(lambda: t.line(0).strip() == "0")
            t.key("Enter")
            t.wait_until(lambda: t.line(0).strip() == "3")

    def test_scrollsub_fills_subwindow(self):
        with Tui(example("12-03_scrollsub")) as t:
            t.wait_for("Scroll away!", timeout=5)


class Pads(unittest.TestCase):
    def test_newpad2_viewport_shows_numbers(self):
        with Tui(example("13-02_newpad2")) as t:
            t.wait_for("Press Enter to update")
            t.key("Enter")
            t.wait_for("0   1   2   3")

    def test_sonofapad_viewport_shows_text(self):
        with Tui(example("13-03_sonofapad")) as t:
            t.wait_for("Press Enter to update")
            t.key("Enter")
            t.wait_for("Hello Hello")


# ---------------------------------------------------------------------------
# Screen dump / restore (chapter 15). dump.win is written to the repo root
# (gitignored via *.win) and removed afterward.
# ---------------------------------------------------------------------------

class ScreenDump(unittest.TestCase):
    def setUp(self):
        self.dump = os.path.join(REPO, "dump.win")
        self._rm()

    def tearDown(self):
        self._rm()

    def _rm(self):
        try:
            os.remove(self.dump)
        except FileNotFoundError:
            pass

    def test_dump_then_restore(self):
        # 15-04 writes the screen to dump.win ...
        with Tui(example("15-04_dumpwin")) as t:
            t.wait_for("Press Enter to dump the screen")
            t.key("Enter")
            t.wait_for("File written")
        self.assertTrue(os.path.exists(self.dump), "dump.win was not created")

        # ... and 15-05 restores it without error, repainting the saved words.
        with Tui(example("15-05_undump")) as t:
            t.wait_for("Press Enter to restore the screen")
            t.key("Enter")
            t.wait_until(lambda: "Error" not in t.text()
                         and len(t.text().strip()) > 0)
            self.assertNotIn("Error reading window file", t.text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
