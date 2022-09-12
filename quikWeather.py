#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# From        : automate the boring stuff.pdf
# DESCRIPTION : Prints weather for a location from command line
# ----------------------------------------------------------------------------

import json
import requests
import optparse
from time import sleep

# location = 2502939                            # Bou ismail location
# api_key = 2dde6a760c607e984dd9e56aa4335d51    # API Key


def collectInformation(location, api_key):
    # Download the json data from openWeatherMap.org's API
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&APPID={}'.format(location, api_key)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as err:
        print('[-] There was a problem: {}'.format(err))
        exit(1)

    # Load JSON data into Python variable.
    weather_data = json.loads(response.text)
    # Load JSON data into file
    # with open('/home/dabve/desktop/weatherAll.json', 'w') as outfile:
    #     json.dump(weather_data, outfile)
    #     outfile.close()
    # Print weather descriptions
    w = weather_data['list']
    city = weather_data['city']     # Take the city name.

    # Print information
    print('Welcom To QuikWeather')
    print('This Script Prints Weather From Openweather.org')
    print()
    print('City Name: {}'.format(city['name']))
    print('Country  : {}\n'.format(city['country']))
    for i in range(0, 40, 4):
        print('[*] Weather: ')
        print('\tAT: ', w[i]['dt_txt'])
        print('\t', w[i]['weather'][0]['main'], '-', w[i]['weather'][0]['description'])
        print('\tHumidity: {}'.format(w[i]['main']['humidity']))
        print('\tTemp min: {}'.format(w[i]['main']['temp_min']))
        print('\tTemp max: {}'.format(w[i]['main']['temp_max']))
        print()
        sleep(1)


def main():
    parser = optparse.OptionParser('Usage: %prog -l <location> -a <API key>')
    parser.add_option('-l', dest='location', type='string', help='Specify Location To get weather')
    parser.add_option('-a', dest='api_key', type='string', help='Get API Key From openweather.org')
    (options, args) = parser.parse_args()
    location = options.location
    api_key = options.api_key
    if location is None or api_key is None:
        print(parser.usage)
        exit(1)
    else:
        collectInformation(location, api_key)


if __name__ == '__main__':
    main()
