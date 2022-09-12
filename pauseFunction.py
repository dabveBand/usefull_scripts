#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DESC : a pause functions to work with helps

import os


def pause(title=''):
    """
    Pause terminal until ENTER is pressed
    title: Title of the pause function.from
    """
    try:
        print('Ctrl-C : Quit\nEnter  : < {} >'.format(title), end='')
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        exit()
