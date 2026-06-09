#include <ncurses.h>

int main()
{
    initscr();

#ifdef NCURSES_MOUSE_VERSION
    addstr("Mouse Functions Available.\n");
    mousemask(ALL_MOUSE_EVENTS, NULL);
    addstr("Mouse Active");
    refresh();
    getch();
#else
    addstr("Mouse Functions Unavailable.\n");
    refresh();
    getch();
#endif

    endwin();
    return 0;
}
