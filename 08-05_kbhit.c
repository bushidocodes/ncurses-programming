#include <ncurses.h>

/**
 * Non-blocking call to check if the keyboard queue has any characters
 */
int kbhit()
{
    int rc;

    nodelay(stdscr, true);
    noecho();

    int ch = getch();
    if (ch == ERR)
        rc = false;
    else
    {
        rc = true;
        ungetch(ch);
    }

    echo();
    nodelay(stdscr, false);
    return rc;
}

int main()
{
    initscr();

    addstr("Tap a key while I count...\n");

    bool did_hit = false;

    for (int i = 0; i < 21; i++)
    {
        printw("%2d ", i);
        refresh();
        napms(500);
        if ((did_hit = kbhit()))
            break;
    }

    addstr("\nDone!\n");

    if (did_hit)
    {
        printw("You pressed the %c key\n", getch());
    }
    else
    {
        printw("Out of time!\n");
    }

    refresh();
    getch();

    endwin();
    return 0;
}
