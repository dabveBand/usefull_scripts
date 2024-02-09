#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------

from rich.console import Console
console = Console()
import time

counter = 1


def do_work(counter):
    while counter != 10:
        time.sleep(0.5)
        print(counter)
        counter += 1


# with console.status('Working...'):
    # do_work(counter)


with console.status('Working...', spinner='monkey'):
    do_work(counter)
