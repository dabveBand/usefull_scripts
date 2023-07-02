#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 09-December-2022
#
# description   : This script based on rich
# ----------------------------------------------------------------------------

import os
from rich import inspect
from rich.console import Console
from rich.markdown import Markdown

console = Console()
menu = Markdown("""
## Python reminder for:
    1. Strings
    2. Lists
    3. Dicts
    4. Tuples
    5. Set

    0. Exit
""")
choices = {'1': str, '2': list, '3': dict, '4': tuple, '5': set}
bye_msg = '\n[bold cyan]Bye[/bold cyan]'


if __name__ == '__main__':
    while True:
        try:
            console.print(menu)
            question = input('\n[?] Choice: ')
            if question == '0':
                console.print(bye_msg)
                break
            try:
                os.system('clear')
                console.print(inspect(choices[question], help=True, methods=True))
            except KeyError:
                pass
        except KeyboardInterrupt:
            console.print(bye_msg)
            break
