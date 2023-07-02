#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DESC    : find the longitude and latitude for a given city name
# ----------------------------------------------------------------
import os
import dotenv
import click
import requests

dotenv.load_dotenv()
API_KEY = os.getenv('MAPQUESTAPI')


@click.command()
@click.argument('location')
def find_city_info(location):
    """
    Retrieve and display information about a city.

    Args:
        location (str): The location (city) to search for.

    Returns:
        None
    """
    url = 'http://www.mapquestapi.com/geocoding/v1/address'
    params = {'key': API_KEY, 'location': location}

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
    find_city_info()
