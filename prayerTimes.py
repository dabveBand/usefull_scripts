#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------

import requests

methods = {
    1: 'University of Islamic Sciences, Karachi',
    2: 'Islamic Society of North America',
    3: 'Muslim World League',
    4: 'Umm Al-Qura University, Makkah',
    5: 'Egyptian General Authority of Survey',
    7: 'Institute of Geophysics, University of Tehran',
    8: 'Gulf Region',
    9: 'Kuwait',
    10: 'Qatar',
    11: 'Majlis Ugama Islam Singapura, Singapore',
    12: 'Union Organization islamic de France',
    13: 'Diyanet İşleri Başkanlığı, Turkey',
    14: 'Spiritual Administration of Muslims of Russia',
}


def get_prayer_times(country, city, month, year, method):
    # http://api.aladhan.com/v1/timingsByCity?city=Bouismail&country=DZ&method=3
    url = 'http://api.aladhan.com/v1/calendarByCity'
    params = {'country': country, 'city': city, 'month': month, 'year': year, 'method': method}
    res = requests.get(url, params=params)
    return res.json()


def print_times_byday(day, jsondata):
    data = jsondata['data']
    day = day - 1               # start from 0 like list index
    by_day = data[day]['timings']

    day_name = data[day]['date']['gregorian']['weekday']['en']
    gregorian = data[day]['date']['readable']
    hijri_d = data[day]['date']['hijri']['day']
    hijri_m = data[day]['date']['hijri']['month']['en']
    hijri_y = data[day]['date']['hijri']['year']
    hijri = '{} {} {}'.format(hijri_d, hijri_m, hijri_y)

    prayers = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    maxkey = max(len(item) for item in prayers)
    to_print = '{} {} -- {}'.format(day_name, gregorian, hijri)
    print()
    print(to_print)
    print('=' * len(to_print))
    for salat in prayers:
        print('   {:{maxkey}} : {}'.format(salat, by_day[salat], maxkey=maxkey))


if __name__ == '__main__':
    from datetime import date
    country = 'DZ'
    city = 'Bouismail'
    method = '3'
    month = input('(?) Month Number: ')
    day = int(input('(?) Day Number: '))
    year = date.today().year
    json_data = get_prayer_times(country, city, month, year, method)
    print_times_byday(day, json_data)
