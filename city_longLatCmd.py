#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DESC    : find the longitude and latitude for a given city name
# ----------------------------------------------------------------
import requests


def find_city_info(location):
    location = location
    api_key = '0VWDo79OAhkZjFc4iItl0UfCSYdo6QbZ'
    url = 'http://www.mapquestapi.com/geocoding/v1/address'
    params = {'key': api_key, 'location': location}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
    except Exception as err:
        print('(-) Err: ', err)
    else:
        city_info = res.json()['results'][0]['locations'][0]
        if city_info['adminArea5'] == '':
            print('  - City     : {} {}'.format(city_info['adminArea4'], city_info['adminArea3']))
        else:
            print('  - City     : {} {}'.format(city_info['adminArea5'], city_info['adminArea3']))

        print('(+) Latitude : {}'.format(city_info['latLng']['lat']))
        print('(+) Longitude: {}'.format(city_info['latLng']['lng']))


if __name__ == '__main__':
    from sys import argv
    if len(argv[1:]) == 1:
        location = argv[1]
    else:
        location = input('\n(?) Enter Locaion: ')

    print()
    print('(*) Information about: {}\n'.format(location))
    find_city_info(location)
    print()
