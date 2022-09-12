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
from colors import Colors

color = Colors()


def get_hijri_date():
    tday = date.today()
    hijri = HijriDate(tday.year, tday.month, tday.day, gr=True)
    return '{} {} {} {}'.format(color.bold_msg(hijri.day_name),
                                color.boldgreen_msg(hijri.day),
                                color.bold_msg(hijri.month_name),
                                color.boldgreen_msg(hijri.year)
                                )


def hijri_date_terminal():
    """
    # print hijri date in terminal with colors
    """
    tday = get_hijri_date()
    print()
    print(tday)
    print()


if __name__ == '__main__':
    hijri_date_terminal()
