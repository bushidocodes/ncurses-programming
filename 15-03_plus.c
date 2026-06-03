#include <ncurses.h>

int main()
{
    initscr();
    curs_set(0);

    move(0, COLS / 2);
    vline(0, LINES);

    move(LINES / 2, 0);
    hline(0, COLS);

    move(LINES / 2, COLS / 2);
    addch(A_ALTCHARSET | 'n');

    refresh();
    getch();

    endwin();
    return 0;
}
