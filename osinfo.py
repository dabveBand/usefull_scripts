#!/usr/bin/env python3

# Script Name       : osinfo.py
# Authors           : 'geekcomputers': 'Craig Richards'
# Created           : 5th April 2012
# Last Modified     : July 19 2016
# Version           : 1.0
# Description       : Displays information about the OS, running this script on

import platform as pl
from colorama import init

init()
profile = [
    'architecture',
    'linux_distribution',
    'mac_ver',
    'machine',
    'node',
    'platform',
    'processor',
    'python_build',
    'python_compiler',
    'python_version',
    'release',
    'system',
    'version',
    'uname'
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


maxkey = max(len(key) for key in profile)
print('\n[*] Information About This Machine:\n')

for key in profile:
    if hasattr(pl, key):
        print('   [+] {:{length}} : {}{}{}'.format(key.title(), bcolors.BOLD, str(getattr(pl, key)()), bcolors.ENDC, length=maxkey))
