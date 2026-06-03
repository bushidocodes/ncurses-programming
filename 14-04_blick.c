#include <ncurses.h>

int main()
{
    initscr();
    noecho();
    keypad(stdscr, TRUE);
    mousemask(ALL_MOUSE_EVENTS, NULL);

    if (!NCURSES_MOUSE_VERSION)
    {
        addstr("Mouse Functions Unavailable.\n");
        refresh();
        getch();
        goto done;
    }

    while (true)
    {
        int ch = getch();
        if (ch == KEY_MOUSE)
        {
            clear();
            MEVENT mort;
            getmouse(&mort);
            switch (mort.bstate)
            {
            case BUTTON1_PRESSED:
                mvaddstr(0, 0, "B1 Press");
                break;
            case BUTTON1_RELEASED:
                mvaddstr(1, 0, "B1 Release");
                break;
            case BUTTON1_CLICKED:
                mvaddstr(2, 0, "B1 Click");
                break;
            case BUTTON1_DOUBLE_CLICKED:
                mvaddstr(3, 0, "B1 2xClick");
                break;
            case BUTTON2_PRESSED:
                mvaddstr(0, 20, "B2 Press");
                break;
            case BUTTON2_RELEASED:
                mvaddstr(1, 20, "B2 Release");
                break;
            case BUTTON2_CLICKED:
                mvaddstr(2, 20, "B2 Click");
                break;
            case BUTTON2_DOUBLE_CLICKED:
                mvaddstr(3, 20, "B2 2xClick");
                break;
            case BUTTON3_PRESSED:
                mvaddstr(0, 40, "B3 Press");
                break;
            case BUTTON3_RELEASED:
                mvaddstr(1, 40, "B3 Release");
                break;
            case BUTTON3_CLICKED:
                mvaddstr(2, 40, "B3 Click");
                break;
            case BUTTON3_DOUBLE_CLICKED:
                mvaddstr(3, 40, "B3 2xClick");
                break;
            case REPORT_MOUSE_POSITION:
                mvaddstr(3, 60, "POS");
                break;
            default:
                break;
            }

            mvaddch(mort.y, mort.x, '*');
            refresh();
            continue;
        }
        if (ch == '\n')
            break;
    }

done:
    endwin();
    return 0;
}
