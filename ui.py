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
    
    def build_tasklists(self, list_id=None, start=0, offset=(2, 4)):
        """Ui for displaying all user's tasklists

        """
        curses.curs_set(0)
        curses.noecho()
        self.tasklists = self.gotask.list_tasklists()
        nb_tasklists = len(self.tasklists)
        if list_id is not None:
            for i in range(nb_tasklists):
                if list_id == self.tasklists[i]['id']:
                    start = i
        opt = start
        offset_y, offset_x = offset
        select = -1
        while select < 0:
            self.screen.clear()
            self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
            self.screen.addstr(offset_y+2, offset_x, 'Please select one tasklist for more details...', curses.A_BOLD)
            for i in range(nb_tasklists):
                if i == opt:
                    self.screen.addstr(offset_y+i+4, offset_x, '-> ' + str(i+1) + '. ' + self.tasklists[i]['title'], curses.color_pair(1))
                else:
                    self.screen.addstr(offset_y+i+4, offset_x+3, str(i+1) + '. ' + self.tasklists[i]['title'])
            self.screen.addstr(offset_y+nb_tasklists+4, offset_x, '(<Enter>: watch list  <r>: refresh list, <u>: update list name, <d>: delete list, <n>: new list..., <q>: quit)')
            self.screen.refresh()
            q = self.screen.getch()
            if q == curses.KEY_UP or q == ord('k'):  # KEY_UP or 'k' on vi/vim mode
                opt = (opt - 1) % (nb_tasklists)
            elif q == curses.KEY_DOWN or q == ord('j'):  # KEY_DOWN or 'j' on vi/vim mode
                opt = (opt + 1) % (nb_tasklists)
            elif q == ord('\n'):
                select = opt
            elif q == ord('n'):  # New a tasklist
                self.new_tasklist(opt)
            elif q == ord('u'):  # Update the selected list name
                self.rename_tasklist(opt)
            elif q == ord('r'):  # Refresh lists
                self.build_tasklists()
            elif q == ord('d'):  # Delete the selected list
                tasklist_id = self.tasklists[opt]['id']
                self.gotask.del_tasklist(tasklist_id)
                self.build_tasklists()
            elif q == ord('q'):
                self.quit()
        curses.endwin()

    def rename_tasklist(self, select, offset=(2, 4)):
        """Ui for renaming a tasklist

        """
        offset_y, offset_x = offset
        curses.curs_set(1)
        curses.echo()
        self.screen.clear()
        self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
        self.screen.addstr(offset_y+2, offset_x, 'Please rename the tasklist. Press <Enter> to return.', curses.A_BOLD)
        self.screen.addstr(offset_y+4, offset_x, 'old list name: ' + self.tasklists[select]['title'])
        self.screen.addstr(offset_y+5, offset_x, 'new list name: ')
        self.screen.refresh()
        new_title = self.screen.getstr()
        if new_title != '':
            self.gotask.rename_tasklist(self.tasklists[select], new_title)
        self.build_tasklists(None, select)

    def new_tasklist(self, select, offset=(2, 4)):
        """Ui for creating a new tasklist

        """
        offset_y, offset_x = offset
        curses.curs_set(1)
        curses.echo()
        self.screen.clear()
        self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
        self.screen.addstr(offset_y+2, offset_x, 'Please give a name to the new list. Press <Enter> to return.', curses.A_BOLD)
        self.screen.addstr(offset_y+4, offset_x, 'new list name: ')
        self.screen.refresh()
        new_title = self.screen.getstr()
        new_tasklist_id = None
        if new_title != '':
            new_tasklist_id = self.gotask.new_tasklist(new_title)
        self.build_tasklists(new_tasklist_id, select)

    def quit(self):
        curses.endwin()
        sys.exit(0)



        
if __name__ == '__main__':
    ui = Ui()
    ui.build_tasklists()
