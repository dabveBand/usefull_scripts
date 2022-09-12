#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# desc    : use figlet cmdline from python
# -----------------------------------------

import subprocess

# figlet_fonts = [slant, shadow, small, smslant, smshadow, big, controlfiles, frango, ivrit, standard, script, terminal, digital,
#                 bubble, lean, block, mini, banner]
# best font = mini, script, banner
# All font use command: $ showfigfont | $ figlist
font_name = 'big'


def figlet_py(msg):
    command = ['figlet', '-kf', font_name, msg]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    except FileNotFoundError:
        print('[-] Error: Command Not Found')
    else:
        p.wait()                    # wait for the process
        out, err = p.communicate()
        if err: print('[-] Error: ', err)
        else: print(out)


if __name__ == '__main__':
    figlet_py('by  el3arbi')
