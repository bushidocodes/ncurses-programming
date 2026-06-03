#define _XOPEN_SOURCE_EXTENDED 1
#include <ncurses.h>
#include <locale.h>

int main(){
	cchar_t heart = {A_NORMAL, {L'\u2615'}, 0};

	setlocale(LC_ALL, "");

	initscr();

	addstr("I ");
	add_wch(&heart);
	addstr(" Ncurses");
	refresh();
	getch();

	endwin();
	return 0;
}
