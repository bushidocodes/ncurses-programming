# ncurses Programming Examples

A collection of 100 C programs written while working through *Dan Gookin's Guide to Ncurses Programming*. Each file is a self-contained example demonstrating a specific ncurses feature, organized by chapter.

## Build

Requires GCC and the wide-character ncurses library (`libncursesw-dev`).

```bash
# Install on Debian/Ubuntu
sudo apt install gcc libncursesw5-dev

# Build all 100 programs into bin/
make

# Remove binaries
make clean
```

On Windows, compile via WSL (Ubuntu 24.04 tested).

Run any example from the `bin/` directory in a terminal that supports ncurses (any standard Linux terminal or WSL terminal):

```bash
bin/09-06_quad
```

---

## Chapter 00 — Introduction

| File | Description |
|------|-------------|
| [00-01_box.c](00-01_box.c) | Draws a border around `stdscr` using `box()`. The first ncurses program. |

---

## Chapter 01 — Hello, ncurses

| File | Description |
|------|-------------|
| [01-01_goodbye.c](01-01_goodbye.c) | Prints "Goodbye, cruel world!" — the minimal ncurses program skeleton: `initscr`, `addstr`, `getch`, `endwin`. |

---

## Chapter 02 — Input and Output

| File | Description |
|------|-------------|
| [02-02_add1.c](02-02_add1.c) | Prints characters one at a time with 100 ms delays using `addch` and `napms`. |
| [02-03_add2.c](02-03_add2.c) | Concatenates two strings and displays the result with `addstr`. |
| [02-04-add3.c](02-04-add3.c) | Same as above but uses `move()` to reposition the cursor before printing. |
| [02-05_yoda.c](02-05_yoda.c) | Formatted output with `printw` — displays Yoda's age. |
| [02-06_typewriter.c](02-06_typewriter.c) | Reads keypresses in a loop with `getch`; exits on `~`. Demonstrates raw character input. |
| [02-07_yourname.c](02-07_yourname.c) | Collects first and last name with `getnstr`, enforcing buffer limits. |
| [02-08_sushi.c](02-08_sushi.c) | Calculates a sushi order total using `scanw` for integer input. |

---

## Chapter 03 — Colors and Attributes

| File | Description |
|------|-------------|
| [03-01_twinkle.c](03-01_twinkle.c) | Cycles text through `A_BOLD`, `A_BLINK`, and `A_NORMAL` attributes. |
| [03-02_annoy.c](03-02_annoy.c) | Displays words with alternating `A_BOLD` and `A_UNDERLINE`. |
| [03-03_colortest.c](03-03_colortest.c) | Checks terminal color support with `has_colors()` before calling `start_color()`. |
| [03-04_yellowred.c](03-04_yellowred.c) | Defines one color pair (`COLOR_YELLOW` on `COLOR_RED`) and applies it. |
| [03-05_colorful.c](03-05_colorful.c) | Multiple color pairs: black-on-red and bold yellow-on-black. |
| [03-06_pink.c](03-06_pink.c) | Creates a custom "pink" color with `init_color(COLOR_RED, 1000, 750, 750)`. |
| [03-07_bgcolor1.c](03-07_bgcolor1.c) | Sets the screen background color with `bkgd()`. |
| [03-08_bgcolor2.c](03-08_bgcolor2.c) | Applies several background color changes in sequence. |
| [03-09_notice.c](03-09_notice.c) | Demonstrates `beep()` for an audible alert and `flash()` for a visual flash. |

---

## Chapter 04 — Characters and Attributes

| File | Description |
|------|-------------|
| [04-01_charattrib.c](04-01_charattrib.c) | Displays every text attribute: STANDOUT, UNDERLINE, REVERSE, BLINK, DIM, BOLD, ALTCHARSET, INVIS, PROTECT, and the extended set. |
| [04-02_changechar.c](04-02_changechar.c) | Uses `addch` with attributes and `move()` to place styled individual characters. |
| [04-03_attrtest.c](04-03_attrtest.c) | Extended version of `04-01` — comprehensive attribute showcase. |
| [04-04_pi.c](04-04_pi.c) | Renders the π symbol using the ACS alternative character set (`ACS_PI`). |
| [04-05_acslist.c](04-05_acslist.c) | Iterates through ACS codes 0–127, printing each symbol. |
| [04-06_acsstring.c](04-06_acsstring.c) | Renders an entire string in the ACS character set using `A_ALTCHARSET`. |
| [04-07_aBox.c](04-07_aBox.c) | Draws a box manually with ACS line-drawing characters (ULCORNER, HLINE, VLINE, etc.). |
| [04-08_chtypestring.c](04-08_chtypestring.c) | Builds a `chtype` array where each cell carries its own attribute, then displays it. |
| [04-09_addchstr.c](04-09_addchstr.c) | Adds an entire pre-attributed `chtype` string at once with `addchstr()`. |
| [04-10_boxarray.c](04-10_boxarray.c) | Draws an ASCII-art box from a character array. |
| [04-11_unicode.c](04-11_unicode.c) | Displays the Unicode coffee-cup character ☕ (U+2615) via `cchar_t` and `wadd_wch`. Requires `-lncursesw`. |
| [04-12_ustring.c](04-12_ustring.c) | Prints the Russian word "привет" (hello) as a wide-character string with `addwstr`. |

---

## Chapter 05 — Screen and Cursor Positioning

| File | Description |
|------|-------------|
| [05-01_screensize.c](05-01_screensize.c) | Reads terminal dimensions with `getmaxy()` / `getmaxx()` and prints them. |
| [05-02_stdscrsize.c](05-02_stdscrsize.c) | Equivalent using the `LINES` and `COLS` macros. |
| [05-03_corners.c](05-03_corners.c) | Places `*` in all four corners with 500 ms pauses using `mvaddch`. |
| [05-03_ncurses.c](05-03_ncurses.c) | Variant of `05-02` — prints window dimensions. |
| [05-04_ctitle.c](05-04_ctitle.c) | `center()` helper that calculates horizontal indent to center a string on screen. |
| [05-05_whereami.c](05-05_whereami.c) | Tracks and displays the cursor's current row/col with `getcury()` / `getcurx()`. |

---

## Chapter 06 — Text Manipulation

| File | Description |
|------|-------------|
| [06-01_text1.c](06-01_text1.c) | Fills the screen with alternating lines of text. |
| [06-02_text2.c](06-02_text2.c) | Inserts a blank line above existing text with `insertln()`. |
| [06-03_text3.c](06-03_text3.c) | Inserts two blank lines and then writes into them. |
| [06-04_text4.c](06-04_text4.c) | Inserts text at a specific position within existing content. |
| [06-05_marquee1.c](06-05_marquee1.c) | Typewriter effect: builds a string right-to-left using `insch()`. |
| [06-06_marquee2.c](06-06_marquee2.c) | Extends the marquee with an alphabet header row. |
| [06-07_text5.c](06-07_text5.c) | Uses `insstr()` to insert a whole string at the cursor position. |
| [06-08_text6.c](06-08_text6.c) | Deletes an entire line with `deleteln()`. |
| [06-09_text7.c](06-09_text7.c) | Deletes individual characters with `delch()`. |
| [06-10_cat.c](06-10_cat.c) | Word replacement: removes one word character-by-character then inserts another with `delch`/`insch`. |
| [06-11_insdel.c](06-11_insdel.c) | Insert/delete multiple rows at once with `insdelln()`. |

---

## Chapter 07 — Screen Clearing

| File | Description |
|------|-------------|
| [07-01_cls.c](07-01_cls.c) | Clears the entire screen with `clear()`. |
| [07-02_clearline.c](07-02_clearline.c) | Clears from the cursor to end-of-line with `clrtoeol()`. |
| [07-03_clearbot.c](07-03_clearbot.c) | Clears from the cursor to bottom-of-screen with `clrtobot()`. |

---

## Chapter 08 — Keyboard Input

| File | Description |
|------|-------------|
| [08-01_yourname.c](08-01_yourname.c) | Name input with a confirmation loop — re-prompts until the user answers `y`. |
| [08-02_keywait1.c](08-02_keywait1.c) | Uses `nodelay()` for non-blocking input; increments a counter while waiting. |
| [08-03_keywait2.c](08-03_keywait2.c) | Counts in a tight loop until the spacebar is pressed (non-blocking mode). |
| [08-04_secretkey.c](08-04_secretkey.c) | Reads two keypresses and checks they match; the second is read with `noecho()`. |
| [08-05_kbhit.c](08-05_kbhit.c) | Implements a `kbhit()` function (DOS-style) using `nodelay` and `ungetch`. |
| [08-06_arrowkeys.c](08-06_arrowkeys.c) | Enables `keypad(stdscr, TRUE)` to receive `KEY_UP`/`DOWN`/`LEFT`/`RIGHT`. |
| [08-07_greetings.c](08-07_greetings.c) | Gets first and last name with `getnstr`. |
| [08-08_urpwd.c](08-08_urpwd.c) | Username/password form: password field uses `noecho()` to hide input. |
| [08-09_flush.c](08-09_flush.c) | Demonstrates `flushinp()` — discards pending input accumulated during a delay. |

---

## Chapter 09 — Windows

| File | Description |
|------|-------------|
| [09-01_anotherwin.c](09-01_anotherwin.c) | Creates a second full-screen window with `newwin(0, 0, 0, 0)`. |
| [09-02_switch.c](09-02_switch.c) | Two windows with different background colors (blue `stdscr`, red overlay). |
| [09-03_switchback.c](09-03_switchback.c) | Uses `touchwin()` to force a full redraw when switching focus between windows. |
| [09-04_touch.c](09-04_touch.c) | Small centered window; `touchwin()` marks it dirty to trigger a refresh. |
| [09-05_halfpint.c](09-05_halfpint.c) | Creates a half-size window positioned at the screen center. |
| [09-06_quad.c](09-06_quad.c) | Divides the screen into four quadrant windows, each with a distinct color. |
| [09-07_twowin.c](09-07_twowin.c) | Two full-height side-by-side windows; demonstrates `delwin()` to release one. |
| [09-08_border.c](09-08_border.c) | Draws a border on `stdscr` with `border()` using default line-drawing chars. |
| [09-09_aborder.c](09-09_aborder.c) | Custom border using comma characters for all eight border positions. |
| [09-10_box.c](09-10_box.c) | Draws the standard box border with `box(stdscr, 0, 0)`. |
| [09-11_quadborders.c](09-11_quadborders.c) | Four quadrant windows, each with its own `box()` border. |

---

## Chapter 10 — Subwindows

| File | Description |
|------|-------------|
| [10-01_sub1.c](10-01_sub1.c) | Creates a subwindow inside a bordered `stdscr` with `subwin()`. |
| [10-02_sub2.c](10-02_sub2.c) | Centered subwindow inside a main window. |
| [10-03_sub3.c](10-03_sub3.c) | Uses `derwin()` (derived window) where coordinates are relative to the parent. |
| [10-04_subsub.c](10-04_subsub.c) | Nested derived windows three levels deep: grandpa → father → son. |
| [10-05_delsub.c](10-05_delsub.c) | Creates and then removes a subwindow with `delwin()`. |

---

## Chapter 11 — Window Copying

| File | Description |
|------|-------------|
| [11-01_overwrite1.c](11-01_overwrite1.c) | Copies content from a red window onto a blue one with `overwrite()`. |
| [11-02_overwrite2.c](11-02_overwrite2.c) | Same as above, but calls `touchwin()` so the destination redraws correctly. |
| [11-03_overlay.c](11-03_overlay.c) | `overlay()` — copies only non-blank characters, leaving the background visible. |
| [11-04_copywin.c](11-04_copywin.c) | Copies a rectangular region transparently with `copywin(..., TRUE)`. |
| [11-05_copywin2.c](11-05_copywin2.c) | Same rectangle copy non-transparently with `copywin(..., FALSE)`. |
| [11-06_dup.c](11-06_dup.c) | `dupwin()` — creates an independent copy of a window. |
| [11-07_movewin.c](11-07_movewin.c) | Moves a window to a new screen position with `mvwin()`. |

---

## Chapter 12 — Scrolling

| File | Description |
|------|-------------|
| [12-01_scrolling1.c](12-01_scrolling1.c) | Shows that text naturally wraps but does not scroll by default. |
| [12-02_scrolling2.c](12-02_scrolling2.c) | Enables auto-scroll with `scrollok(stdscr, TRUE)`. |
| [12-03_scrollsub.c](12-03_scrollsub.c) | Enables scrolling within a subwindow. |
| [12-04_scroll.c](12-04_scroll.c) | Manually scrolls the window one line with `scroll()`. |
| [12-05_scrup3.c](12-05_scrup3.c) | Scrolls three lines at once with `scrl(3)`. |
| [12-06_scrollreg.c](12-06_scrollreg.c) | Restricts scrolling to a middle band using `setscrreg()`. |

---

## Chapter 13 — Pads

| File | Description |
|------|-------------|
| [13-01_newpad1.c](13-01_newpad1.c) | Creates a pad (virtual window larger than the screen) with `newpad()`. |
| [13-02_newpad2.c](13-02_newpad2.c) | Fills a pad with data and displays a viewport into it with `prefresh()`. |
| [13-03_sonofapad.c](13-03_sonofapad.c) | Creates a sub-pad inside a pad with `subpad()`. |

---

## Chapter 14 — Mouse

| File | Description |
|------|-------------|
| [14-01_mousetest.c](14-01_mousetest.c) | Checks mouse support via `NCURSES_MOUSE_VERSION` and `mousemask()`. |
| [14-02_mspy.c](14-02_mspy.c) | Reports real-time mouse coordinates (row, col) as the cursor moves. |
| [14-03_clickput.c](14-03_clickput.c) | Places a `*` wherever the user clicks using `BUTTON1_CLICKED`. |
| [14-04_blick.c](14-04_blick.c) | Detects and labels button states: PRESSED, RELEASED, CLICKED, DOUBLE_CLICKED for buttons 1–3. |

---

## Chapter 15 — Miscellaneous

| File | Description |
|------|-------------|
| [15-01_curset.c](15-01_curset.c) | Cycles the cursor through invisible, normal, and very visible with `curs_set(0/1/2)`. |
| [15-02_steps.c](15-02_steps.c) | Draws diagonal and horizontal lines using `hline()` and `vline()`. |
| [15-03_plus.c](15-03_plus.c) | Draws a centered crosshair using `hline`/`vline` with ACS line characters. |
| [15-04_dumpwin.c](15-04_dumpwin.c) | Saves the current screen to a file with `scr_dump("dump.win")`. |
| [15-05_undump.c](15-05_undump.c) | Restores a previously saved screen from file with `scr_restore("dump.win")`. |

---

## ncurses API Quick Reference

| Function | Purpose |
|----------|---------|
| `initscr()` / `endwin()` | Initialize and tear down ncurses |
| `addch()` / `addstr()` / `printw()` | Output a character, string, or formatted text |
| `mvaddch()` / `mvaddstr()` | Move cursor then output |
| `getch()` / `getnstr()` / `scanw()` | Read a key, bounded string, or formatted input |
| `attron()` / `attroff()` / `attrset()` | Enable/disable/replace text attributes |
| `start_color()` / `init_pair()` / `COLOR_PAIR()` | Set up and apply color pairs |
| `init_color()` | Define a custom color (requires terminal support) |
| `bkgd()` | Set window background character and attributes |
| `newwin()` / `delwin()` | Create and destroy a window |
| `subwin()` / `derwin()` | Create a subwindow (absolute or parent-relative coords) |
| `refresh()` / `wrefresh()` / `touchwin()` | Push virtual screen to terminal |
| `move()` / `wmove()` | Position the cursor |
| `clear()` / `clrtoeol()` / `clrtobot()` | Erase screen regions |
| `insertln()` / `deleteln()` / `insch()` / `delch()` | Insert/delete lines and characters |
| `scrollok()` / `scroll()` / `scrl()` / `setscrreg()` | Control scrolling |
| `newpad()` / `prefresh()` / `subpad()` | Pads — virtual windows larger than the screen |
| `mousemask()` / `getmouse()` | Enable and read mouse events |
| `keypad()` / `nodelay()` / `noecho()` | Input mode flags |
| `beep()` / `flash()` | Audible and visual alerts |
| `curs_set()` | Control cursor visibility |
| `hline()` / `vline()` | Draw horizontal/vertical lines |
| `scr_dump()` / `scr_restore()` | Save and restore screen state |
| `box()` / `border()` | Draw a border around a window |
| `overwrite()` / `overlay()` / `copywin()` / `dupwin()` | Copy window content |
| `napms()` | Sleep for N milliseconds |
