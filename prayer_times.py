#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    : prayer_times.py
# caller  : hijri_.py
# author  : Ibrahim Addadi; dabve@gmail.com.
# created : 11-April-2021
# version : 1.0
# ----------------------------------------------------------------------------
# DESC  : get prayer time FROM
#   for a day     : https://api.pray.zone/v2/times/today.json
#   for a week    : https://api.pray.zone/v2/times/this_week.json?city=mecca
#   for a month   : https://api.pray.zone/v2/times/this_month.json?city=mecca
#
# PARAMS FOR URL:
#   + scholl list for this api:
#   NOTE: pass the number in params.
#   + school_lst = {'Ithna Ashari': 0,
#                   'University of Islamic Sciences, Karachi': 1,
#                   'Islamic Society of North America': 2,
#                   'Muslim World League': 3,
#                   'Umm Al-Qura University, Mecca': 4,
#                   'Egyptian General Authority of Survey': 5,
#                   'Institute of Geophysics, University of Tehran': 7,
#                   'Morocco': 8,
#                   'Department of Islamic Advancement, Malaysia (JAKIM)': 9,
#                   'Majlis Ugama Islam Singapura': 10,
#                   'Union des Organisations Islamiques de France': 11,
#                   'Turkey': 12
#                   ]
#
#   + juristic = (0 for Shafii, 1 for Hanafi); default 0
#   + timeformat = (0: '24-hour format(default)', 1: '12-hour format', 2: '12-hour format without am/pm')
# -------------------------------------------------------------------------
import json


def translate_to_arabic(times_):
    times_ = [('الإمساك', times_['Imsak']), ('الشروق', times_['Sunrise']), ('الفجر', times_['Fajr']), ('الظهر', times_['Dhuhr']),
              ('العصر', times_['Asr']), ('المغرب', times_['Maghrib']), ('العشاء', times_['Isha'])]
    return times_


def get_prayer_times(city, school):
    import requests
    url = 'https://api.pray.zone/v2/times/this_month.json'
    params = {'city': city, 'school': school}
    json_ptimes = './prayer_times.json'
    try:
        res = requests.get(url, params)
    except Exception as err:
        print('[!] Error Using Cache File: {}\n'.format(err))
        with open(json_ptimes) as f:
            prayer_times = json.load(f)
    else:
        # times_ keys : ('Imsak', 'Sunrise', 'Fajr', 'Dhuhr', 'Asr', 'Sunset', 'Maghrib', 'Isha', 'Midnight')
        # date_ keys : ('timestamp', 'gregorian', 'hijri')
        # location keys : ('latitude', 'longitude', 'elevation', 'city', 'country', 'country_code', 'timezone', 'local_offset')
        # settings keys : ('timeformat', 'school', 'juristic', 'highlat', 'fajr_angle', 'isha_angle')
        prayer_times = res.json()['results']
        with open(json_ptimes, 'w') as f:
            json.dump(prayer_times, f)

    # this will return 30 item
    return prayer_times


def parse_data(city, school, day_number):
    prayer_times = get_prayer_times(city, school)
    times_ = prayer_times['datetime'][day_number]['times']
    # convert to arabic words
    # ptimes = translate_to_arabic(times_)
    date_ = prayer_times['datetime'][day_number]['date']       # is a dict

    return (times_, date_)


def dump_records(day_number):
    """
    This function is for debugging
    """
    from terminaltables import AsciiTable
    ptimes, date_ = parse_data('bou-ismail', 4, day_number)
    table_data = [['Prayer', 'Times']]                         # append description as table headers
    ptimes_list = [list([key, value]) for key, value in ptimes.items()]
    for row in ptimes_list:
        table_data.append(list(map(str, row)))
    table_instance = AsciiTable(table_data)
    print(table_instance.table)


if __name__ == '__main__':
    day_number = int(input('Day Number: ')) - 1
    dump_records(day_number)
