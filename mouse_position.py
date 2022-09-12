#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------

import sys
import pyautogui


def mouse_position():
    print('Press Ctrl-C to required coordinate.')
    try:
        while True:
            x, y = pyautogui.position()
            pos = 'X: {} ; Y: {}'.format(x, y)
            print(pos, end='')
            print('\b' * len(pos), end='', flush=True)
    except KeyboardInterrupt:
        print('\n\n[+] Position: ({}, {})'.format(x, y))
        sys.exit()


if __name__ == '__main__':
    mouse_position()
