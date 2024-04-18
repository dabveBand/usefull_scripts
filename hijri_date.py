#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =========================================
#  FILE     : hijri_date.py
#  CREATED  : 18-June-2020
#  AUTHOR   : daBve, dabve@outlook.fr
#  DESC     : display hijri date
# =========================================

from ummalqura.hijri_date import HijriDate
from datetime import date
import datetime
from colors import Colors
from rich.console import Console

console = Console()
color = Colors()


def milady2hijri(milady):
    """
    this function take an input format and transform to datetime.strptime and than to hijri ummalqura
    :milady: input time as dd-mm-yyyy
    :return: ummalqure.HijriDate date
    """
    try:
        to_hijri = datetime.datetime.strptime(milady, '%d-%m-%Y')                # 2015-10-21 00:00:00
    except ValueError:
        return 'ValueError'
    else:
        hijri = HijriDate(to_hijri.year, to_hijri.month, to_hijri.day, gr=True)
        return hijri


if __name__ == '__main__':
    #
    # Today's date
    tday = date.today()
    hijri = HijriDate(tday.year, tday.month, tday.day, gr=True)
    console.print(f'\n{tday}\n')
    console.print(f'\n{hijri.day_name} [green]{hijri.day}[/green] {hijri.month_name} {hijri.year}\n', style='bold')

    #  enter in Converting loop
    while True:
        try:
            milady = input('milady example: 21-12-2022: ')
            hijri = milady2hijri(milady)
            if hijri == 'ValueError':
                console.print('\nYou must enter format like this: 01-01-2000\n', style='bold red')
                continue
            console.print(f'\n{hijri.day_name} {hijri.day} {hijri.month_name} {hijri.year}\n', style='bold')
        except KeyboardInterrupt:
            print()
            break
