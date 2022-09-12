#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# description: Launches a map in the browser using an adress from the cmd or clipboard


def main():
    parser = optparse.OptionParser('%prog: --adress <street adress>')
    parser.add_option('--adress', dest='adress', type='string', help='Street address')
    (options, args) = parser.parse_args()
    adress = options.adress
    if adress is None:
        # Get adress from clipboard.
        adress = pyperclip.paste()
    else:
        # Get adress from command line.
        adress = options.adress

    webbrowser.open('https://www.google.com/maps/place/' + adress)


if __name__ == '__main__':
    import optparse
    import webbrowser
    import pyperclip
    main()
