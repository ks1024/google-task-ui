#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import sys

from gotask import GoTask

class Ui:

    def __init__(self):
        self.gotask = GoTask()
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.screen.keypad(1)
    
    def build_tasklists(self, start=0, offset=(4, 4)):
        """Build tasklists menu

        """
        curses.curs_set(0)
        curses.noecho()
        self.tasklists = self.gotask.list_tasklists()
        nb_tasklists = len(self.tasklists)
        opt = start
        offset_y, offset_x = offset
        select = -1
        while select < 0:
            self.screen.clear()
            self.screen.addstr(2, offset_x, "Term - Google Task")
            self.screen.addstr(offset_y, offset_x, "Please select one tasklist for more details...", curses.A_BOLD)
            for i in range(nb_tasklists):
                if i == opt:
                    self.screen.addstr(offset_y+i+1, offset_x, '-> ' + str(i+1) + '. ' + self.tasklists[i]['title'], curses.color_pair(1))
                else:
                    self.screen.addstr(offset_y+i+1, offset_x+3, str(i+1) + '. ' + self.tasklists[i]['title'])
            self.screen.addstr(offset_y+nb_tasklists+1, 4, '(r: refresh list, u: update list name, d: delete list, n: new list..., q: quit)')
            self.screen.refresh()
            q = self.screen.getch()
            if q == curses.KEY_UP or q == ord('k'):     # KEY_UP or 'k' on vi/vim mode
                opt = (opt - 1) % (nb_tasklists)
            elif q == curses.KEY_DOWN or q == ord('j'): # KEY_DOWN or 'j' on vi/vim mode
                opt = (opt + 1) % (nb_tasklists)
            elif q == ord('\n'):
                select = opt
            elif q == ord('u'):
                self.rename_tasklist(opt)
            elif q == ord('r'):
                self.build_tasklists()
            elif q == ord('q'):
                self.quit()

    def rename_tasklist(self, select, offset=(4, 4)):
        offset_y, offset_x = offset
        curses.curs_set(1)
        curses.echo()
        self.screen.clear()
        self.screen.addstr(2, offset_x, "Term - Google Task UI")
        self.screen.addstr(offset_y, offset_x, "Please rename the tasklist...", curses.A_BOLD)
        self.screen.addstr(offset_y+1, offset_x, 'old list name: ' + self.tasklists[select]['title'])
        self.screen.addstr(offset_y+2, offset_x, 'new list name: ')
        self.screen.refresh()
        new_title = self.screen.getstr(offset_y+2, offset_x+len('new list name:')+1, 50)
        if new_title != '':
            self.gotask.rename_tasklist(self.tasklists[select], new_title)
        self.build_tasklists(select)

    def quit(self):
        curses.endwin()
        sys.exit(0)



        
if __name__ == '__main__':
    ui = Ui()
    ui.build_tasklists()
