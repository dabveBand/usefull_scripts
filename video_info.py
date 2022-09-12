#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    : video_info.py
# desc    : this script is a simple of using youtube-dl as a module
# ---------------------------------------------------------
import youtube_dl
from hurry.filesize import size     # convert file size in human

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

with ydl:
    result = ydl.extract_info('https://www.youtube.com/watch?v=8bu5F678DJ0', download=False)     # extract info no download

if 'entries' in result:
    # can be a playlist or a list of videos
    viedo = result['entries'][0]
else:
    video = result

video_title = video['title']
video_format = video['formats'][0]
file_size = size(int(video_format['filesize']))
print('[+] Title    : {}'.format(video_title))
print('[+] Format   : {}'.format(video_format['format']))
print('[+] File Size: {}'.format(file_size))

# download a video
"""
from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.downlad(['link_to_video'])


# WITH OPTIONS
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s',
    'noplaylist' : True,
    'progress_hooks': [my_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=pwp1CH5R-w4'])

# AS MP3
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
"""
