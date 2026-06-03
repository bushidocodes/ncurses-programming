#include <ncurses.h>

int main()
{
    char text1[] = "This is the first line\n";
    char text3[] = "The third line\n";
    char text5[] = "And the fifth line\n";

    initscr();

    addstr(text1);
    addstr(text3);
    addstr(text5);

    refresh();
    getch();

    move(1, 0);
    insertln();
    refresh();
    getch();

    endwin();

    return 0;
}
