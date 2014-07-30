#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses

class Ui:

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()     # Turn off echo mode 
        curses.curs_set(0)  # Leave cursor invisible
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.screen.keypad(1)


