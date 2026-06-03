#include <ncurses.h>

int main()
{
    char text[] = "This is some wrapping.  ";

    initscr();

    for (int i = 0; i < 300; i++)
    {
        addstr(text);
        napms(100);
        refresh();
    }

    getch();
    endwin();
    return 0;
}
