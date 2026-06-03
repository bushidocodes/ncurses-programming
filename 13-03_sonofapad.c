#include <ncurses.h>

int main()
{
    initscr();

    WINDOW *p = newpad(50, 50);
    if (p == NULL)
    {
        endwin();
        puts("Unable to create pad");
        return 1;
    }

    for (int i = 0; i < 50; i++)
    {
        waddstr(p, "Hello ");
    }

    WINDOW *sp = subpad(p, 10, 10, 0, 0);
    if (sp == NULL)
    {
        delwin(p);
        endwin();
        puts("Unable to create subpad");
        return 1;
    }

    addstr("Press Enter to update");
    refresh();
    getch();

    prefresh(p, 0, 0, 5, 5, 16, 45);
    getch();

    delwin(sp);
    delwin(p);
    endwin();
    return 0;
}
