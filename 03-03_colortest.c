#include <ncurses.h>

int main(){
	initscr();
	int rc = 0;

	if(!has_colors()){
		fprintf(stderr, "Terminal cannot do colors!\n");
		goto DONE;
	}

	if (start_color() != OK) {
		perror("Failed to start colors\n");
		goto ERR_START_COLOR;
	}

	printw("Colors initialized.\n");
	printw("%d colors available.\n", COLORS);
	printw("%d color pairs.", COLOR_PAIRS);
	refresh();
	getch();

DONE:
	endwin();
	return rc;
ERR_START_COLOR:
	rc = 1;
	goto DONE;
}
