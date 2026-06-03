#include <ncurses.h>
#include <string.h>

void center(int row, char *title)
{
    int len = strlen(title);
    int width = getmaxx(stdscr);
    int indent = (width - len) / 2;

    mvaddstr(row, indent, title);
    refresh();
}

int main()
{
    initscr();

    center(1, "Penguin Soccer Finals");
    center(5, "Cattle Dung Samples from Temecula");
    center(7, "Catatonic Theater");
    center(9, "Why do Ions hate each other?");

    getch();

    endwin();
    return 0;
}
