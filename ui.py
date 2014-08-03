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
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
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
            self.screen.addstr(offset_y+nb_tasklists+4, offset_x, 
                    '(<Enter>: watch list  <r>: refresh list, <u>: update list name, <d>: delete list, <n>: new list..., <q>: quit)', curses.color_pair(2))
            self.screen.refresh()
            q = self.screen.getch()
            if q == curses.KEY_UP or q == ord('k'):  # KEY_UP or 'k' on vi/vim mode
                opt = (opt - 1) % nb_tasklists
            elif q == curses.KEY_DOWN or q == ord('j'):  # KEY_DOWN or 'j' on vi/vim mode
                opt = (opt + 1) % nb_tasklists
            elif q == ord('\n'):  # Watch a tasklist
                self.build_tasks(opt)
            elif q == ord('n'):  # New a tasklist
                self.new_tasklist(opt)
            elif q == ord('u'):  # Update the selected tasklist name
                self.rename_tasklist(opt)
            elif q == ord('r'):  # Refresh lists
                self.build_tasklists()
            elif q == ord('d'):  # Delete the selected tasklist
                tasklist_id = self.tasklists[opt]['id']
                self.gotask.del_tasklist(tasklist_id)
                self.build_tasklists()
            elif q == ord('q'):
                self.quit()
        curses.endwin()

    def build_tasks(self, list_num_selected, start=0, offset=(2, 4)):
        """Ui for displaying all tasks of the selected tasklist

        """
        offset_y, offset_x = offset
        select = -1
        curses.curs_set(0)
        curses.noecho()
        tasklist_id = self.tasklists[list_num_selected]['id']
        tasklist_title = self.tasklists[list_num_selected]['title']
        tasks = self.gotask.list_tasks(tasklist_id)
        nb_tasks = len(tasks)
        opt = start
        while select < 0:
            self.screen.clear()
            self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
            self.screen.addstr(offset_y + 2, offset_x, 'Tasks of tasklist - ' + tasklist_title, curses.A_BOLD)
            if nb_tasks == 0:
                self.screen.addstr(offset_y + 4, offset_x, 'Sorry. The list is empty')
                self.screen.addstr(offset_y + 5, offset_x, '<n>: new task, <b>: back to lists, <q>: quit', curses.color_pair(2))
            else:
                for i in range(nb_tasks):
                    info = '';
                    if 'due' in tasks[i]:
                        info = info + ' [due]'
                    if 'notes' in tasks[i]:
                        info = info + ' [notes]'
                    info = info + ' [' + tasks[i]['status'] + ']'
                    if i == opt:
                        self.screen.addstr(offset_y + i + 4, offset_x, '-> ' + str(i+1) + '. ' + tasks[i]['title'] + info, curses.color_pair(1))
                    else:
                        self.screen.addstr(offset_y + i + 4, offset_x + 3, str(i+1) + '. ' + tasks[i]['title'] + info)
                self.screen.addstr(offset_y + nb_tasks + 4, offset_x, '<Enter>: watch task, <n>: new task, <b>: back to lists, <q>: quit', curses.color_pair(2))
            self.screen.refresh()
            q = self.screen.getch()
            if q == curses.KEY_DOWN or q == ord('j'):
                opt = (opt + 1) % nb_tasks
            elif q == curses.KEY_UP or q == ord('k'):
                opt = (opt - 1) % nb_tasks
            elif q == ord('\n'):
                self.build_task(tasks[opt], opt, list_num_selected)
            elif q == ord('n'):
                self.new_task(list_num_selected)
            elif q == ord('b'):
                self.build_tasklists(None, list_num_selected)
            elif q == ord('q'):
                self.quit()

    def build_task(self, task, task_num_selected, list_num_selected, offset=(2, 4)):
        """Ui for displaying the task details

        """
        offset_y, offset_x = offset
        key = -1
        while key < 0:
            self.screen.clear()
            self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
            self.screen.addstr(offset_y + 2, offset_x, 'Task details', curses.A_BOLD)
            if task['title'] == '':
                task['title'] = '<empty>'
            if 'due' not in task:
                task['due'] = '<empty>'
            if 'notes' not in task:
                task['notes'] = '<empty>'
            self.screen.addstr(offset_y + 4, offset_x, 'Title: ' + task['title'])
            self.screen.addstr(offset_y + 5, offset_x, 'Due to: ' + task['due'])
            self.screen.addstr(offset_y + 6, offset_x, 'Notes: ' + task['notes'])
            self.screen.addstr(offset_y + 7, offset_x, 'Status: ' + task['status'])
            self.screen.addstr(offset_y + 8, offset_x, '(<b>: back to list, <q>: quit)', curses.color_pair(2))
            self.screen.refresh()
            q = self.screen.getch()
            if q == ord('b'):
                self.build_tasks(list_num_selected, task_num_selected)
            elif q == ord('q'):
                self.quit()

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
        self.screen.addstr(offset_y + 2, offset_x, 'Please give a name to the new list. Press <Enter> to return.', curses.A_BOLD)
        self.screen.addstr(offset_y + 4, offset_x, 'new list name: ')
        self.screen.refresh()
        new_title = self.screen.getstr()
        new_tasklist_id = None
        if new_title != '':
            new_tasklist_id = self.gotask.new_tasklist(new_title)
        self.build_tasklists(new_tasklist_id, select)

    def new_task(self, list_num_selected, offset=(2, 4)):
        """Ui for creating a new task

        """
        offset_y, offset_x = offset
        curses.curs_set(1)
        curses.echo()
        opt = 0
        title = ''
        due_to = ''
        notes = ''
        while opt < 3: 
            self.screen.clear()
            self.screen.addstr(offset_y, offset_x, 'Term - Google Task')
            self.screen.addstr(offset_y + 2, offset_x, 'Create a new task', curses.A_BOLD)
            self.screen.addstr(offset_y + 4, offset_x, 'Title: ' + title)
            self.screen.addstr(offset_y + 5, offset_x, 'Due to (YYYY-MM-DD): ' + due_to)
            self.screen.addstr(offset_y + 6, offset_x, 'Notes: ' + notes)
            self.screen.refresh()
            if opt == 0:
                title = self.screen.getstr(offset_y + 4, offset_x + 7)
            elif opt == 1:
                due_to = self.screen.getstr(offset_y + 5, offset_x + 21)
            elif opt == 2:
                notes = self.screen.getstr(offset_y + 6, offset_x + 7)
            opt += 1

        tasklist_id = self.tasklists[list_num_selected]['id']
        task = dict()
        task['title'] = title
        if due_to != '':
            task['due'] = due_to + 'T12:00:00.000Z'
        if notes != '':
            task['notes'] = notes
        self.gotask.new_task(tasklist_id, task)
        self.build_tasks(list_num_selected) 

    def quit(self):
        curses.endwin()
        sys.exit(0)



        
if __name__ == '__main__':
    ui = Ui()
    ui.build_tasklists()
