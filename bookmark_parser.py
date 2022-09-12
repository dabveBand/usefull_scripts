#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
#
#         FILE : bookmark_parser.py
#      CREATED : 01-Apr-2019
#       AUTHOR : daBve, dabve@outlook.fr
#
#         DESC : Firefox bookmarks parser
#        USAGE : ./bookmark_parser.py -f <file_name.json>
# ==========================================================

# To get the bookmark file from firefox:
# 1. Ctrl + Shift + O
# 2. import and backup
# 3. backup

# Chrome on windows: C:\Users\UP4\AppData\Local\Google\Chrome\User Data\Profile 2\bookmarks


def decode_json(json_file):
    with open(json_file, encoding='utf-8') as json_file:
        data = json.load(json_file)

    # print(data)
    root = data['roots']
    b_bar = root['bookmark_bar']
    children = b_bar['children']
    for child in children:
        for bmark in child['children']:
            if bmark['type'] == 'folder':
                print('Folder name : ', bmark['name'])
                for i in bmark['children']:
                    print('\tname  :', i['name'])
                    print('\turl   :', i['url'])
                    print('\t-------')
            else:
                print('url   : ', bmark['url'])
                print('name  : ', bmark['name'])
            print('-' * 100)


def main():
    usage = '%prog -f <json file name>'
    parser = optparse.OptionParser(usage=usage, version='%prog 1.0')
    parser.add_option('-f', '--file', metavar='json file', dest='input_json', help='Specify the json file containing bookmarks')
    options, args = parser.parse_args()

    if options.input_json is None:
        print(parser.usage)
    else:
        input_json = options.input_json
        decode_json(input_json)


if __name__ == '__main__':
    import json
    import optparse
    main()
