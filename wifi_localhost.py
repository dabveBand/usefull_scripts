#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       : 06-June-2022
#
# description   : get all wifi password stored in a linux machine
# ----------------------------------------------------------------------------

from pathlib import Path
import colors
color = colors.Colors()


def format_line(title, line):
    print(color.simple_msg('{} : {}{}{}'.format(title, color.BD, line.rstrip().split('=')[1], color.reset)))


system_conn = Path('/etc/NetworkManager/system-connections')
print(color.simple_msg('List of all SSID in this Machine:\n'))
for f in system_conn.iterdir():
    # iterate through system_conn dir
    print(f.name)

print()
ssid_fname = input(color.input_msg('Enter SSID: '))
ssid_fname = system_conn.joinpath(ssid_fname)           # join path with pathlib
try:
    with open(ssid_fname) as f:
        print()
        for line in f:
            if line.startswith('id'):
                format_line('SSID    ', line)
            if line.startswith('key-mgmt'):
                format_line('Key MGMT', line)
            if line.startswith('psk'):
                format_line('Password', line)
except PermissionError:
    print(color.error_msg('run the script as ROOT.'))
