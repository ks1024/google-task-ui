#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses

from gotask import GoTask

class Ui:

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()     # Turn off echo mode 
        curses.curs_set(0)  # Leave cursor invisible
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.screen.keypad(1)
    
    def build_tasklists(self):
        """Build tasklists menu

        """
        gotask = GoTask()
        tasklists = gotask.list_tasklists()
        num_tasklists = len(tasklists)
        opt = 0
        step = 1
        offset = 4
        select = -1
        while select != num_tasklists:
            self.screen.clear()
            self.screen.addstr(2, 4, "Term - Google Task UI")
            self.screen.addstr(offset, 4, "Please select one tasklist for more details...", curses.A_BOLD)
            for i in range(num_tasklists + 1):
                if i < num_tasklists:
                    if i == opt:
                        self.screen.addstr(offset + step + i, 4, '-> ' + str(i+1) + '. ' + tasklists[i]['title'], curses.color_pair(1))
                    else:
                        self.screen.addstr(offset + step + i, 7, str(i+1) + '. ' + tasklists[i]['title'])
                else:
                    if i == opt:
                        self.screen.addstr(offset + step + i, 4, "-> Exit ('q')", curses.color_pair(1))
                    else:
                        self.screen.addstr(offset + step + i, 7, "Exit ('q')")
                    
            self.screen.refresh()
            q = self.screen.getch()
            if q == curses.KEY_UP or q == ord('k'):     # KEY_UP or 'k' on vi/vim mode
                opt = (opt - 1) % (num_tasklists + 1)
            elif q == curses.KEY_DOWN or q == ord('j'): # KEY_DOWN or 'j' on vi/vim mode
                opt = (opt + 1) % (num_tasklists + 1)
            elif q == ord('\n'):
                select = opt
            if q == ord('q') or select == num_tasklists:
                break

        curses.endwin()
        
if __name__ == '__main__':
    ui = Ui()
    ui.build_tasklists()
