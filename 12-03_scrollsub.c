#include <ncurses.h>

int main()
{
    char text[] = "Scroll away! ";

    initscr();

    WINDOW *sub = subwin(stdscr, 10, 30, 6, 24);
    scrollok(sub, true);

    for (int i = 0; i < 35; i++)
    {
        waddstr(sub, text);
        napms(50);
        wrefresh(sub);
    }
    getch();

    endwin();
    return 0;
}
