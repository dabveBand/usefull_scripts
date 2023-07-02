#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    : prayer_times.py
# caller  : hijri_.py
# author  : Ibrahim Addadi; dabve@gmail.com.
# created : 11-April-2021
# version : 1.0
# ----------------------------------------------------------------------------
import salat
import datetime as dt
import pytz
import tabulate


# set up calculation methods
pt = salat.PrayerTimes(salat.CalculationMethod.MWL, salat.AsrMethod.STANDARD)

# January 1, 2000
date = dt.date(2000, 1, 1)
date = dt.datetime.today()

# using NYC
longitude = 2.691420   # degrees East
latitude = 36.643978      # degrees North
eastern = pytz.timezone('Africa/Algiers')

# calculate times
prayer_times = pt.calc_times(date, eastern, longitude, latitude)

# print in a table
table = [["Name", date.strftime('%d/%m/%Y')]]
for name, time in prayer_times.items():
    readable_time = time.strftime("%I:%M")      # %p for am pm
    table.append([name.title(), readable_time])
print(tabulate.tabulate(table, headers='firstrow'))
