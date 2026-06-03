#include <ncurses.h>
#include <string.h>

int main()
{
    char text[] = "Armstrong walks on moon";

    initscr();

    move(5, 0);

    for (char a = 'A'; a < 'Z'; a++)
    {
        addch(a);
        addstr("  ");
    }

    for (int len = strlen(text) - 1; len >= 0; len--)
    {
        move(5, 5);
        insch(*(text + len));
        refresh();
        napms(100);
    }

    getch();

    endwin();

    return 0;
}
