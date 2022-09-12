#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /----------------------------------------------------------------------------
#
#          FILE: youtubeDl.py
#         USAGE: ./youtubeDl.py
#   DESCRIPTION:
#          From:
#        AUTHOR: dabve in Lenovo
#       CREATED: Saturday 05-05-2018
#
# \----------------------------------------------------------------------------

from __future__ import unicode_literals
import youtube_dl
import optparse


def getVideoInfo(url):
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)

    print('[+] upload date : %s' % (meta['upload_date']))
    print('[+] uploader    : %s' % (meta['uploader']))
    print('[+] views       : %d' % (meta['view_count']))
    print('[+] likes       : %d' % (meta['like_count']))
    print('[+] dislikes    : %d' % (meta['dislike_count']))
    print('[+] id          : %s' % (meta['id']))
    print('[+] format      : %s' % (meta['format']))
    print('[+] duration    : %s' % (meta['duration']))
    print('[+] title       : %s' % (meta['title']))
    print('[+] description : %s' % (meta['description']))


def main():
    parser = optparse.OptionParser('Usage: %prog -u <url>',
                                   description='Video Informatin')
    parser.add_option('-u', dest='url', type='string',
                      help='Specify URL')
    (options, args) = parser.parse_args()
    url = options.url
    if url is None:
        print(parser.usage)
        exit(0)
    else:
        getVideoInfo(url)


if __name__ == '__main__':
    main()
