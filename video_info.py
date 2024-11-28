#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : Saturday 05-05-2018
# desc          :
# ----------------------------------------------------------------------------

import yt_dlp       # pip install yt_dlp


def get_video_info(url):
    """
    Get Youtube Video Information
    :url: video url
    """
    ydl_opts = {}       # see help(yt_dlp.YoutubeDL) for a list of available options and public functions

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        # meta is a python dict

    print('-' * 50)
    print('[+] VIDEO INFORMATION:')
    print(f"  [+] ID              : {meta['id']}")
    print(f"  [+] Title           : {meta['title']}")
    print(f"  [+] Format          : {meta['format']}")
    print(f"  [+] Upload date     : {meta['upload_date']}")
    print(f"  [+] Uploader        : {meta['uploader']}")
    print(f"  [+] Views           : {meta['view_count']}")
    print(f"  [+] Likes           : {meta['like_count']}")
    print(f"  [+] Duration        : {meta['duration']}")
    print(f"  [+] Resolution      : {meta['resolution']}")
    print(f"  [+] Language        : {meta['language']}")
    print(f"  [+] Comment Count   : {meta['language']}")
    print(f"  [+] Availability    : {meta['availability']}")
    print(f"  [+] Categories      : {meta['categories']}")
    print(f"  [+] Description     : {meta['description']}")

    print('-' * 50)
    # channel info
    print('[+] CHANNEL INFORMATION:')
    print(f"  [+] Channel ID            : {meta['channel_id']}")
    print(f"  [+] Channel               : {meta['channel']}")
    print(f"  [+] Channel URL           : {meta['channel_url']}")
    print(f"  [+] Channel Follower Count: {meta['channel_follower_count']}")


if __name__ == '__main__':
    url = input('Youtube URL: ')
    get_video_info(url)
