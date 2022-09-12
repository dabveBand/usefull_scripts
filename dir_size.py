#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    : disk_space.py
# author  : Ibrahim Addadi; dabve@gmail.com.
# created : 22-April-2021
# version : 0.1.0
# desc    : Get directory size
# ---------------------------------------------------------
import os
import hurry.filesize     # convert file size in human
import click


def get_dir_size(path, max_files):
    fsize_list = {}
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            fp_size = os.path.getsize(fp)
            fsize_list[fp] = fp_size
    return fsize_list


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=True))
@click.option('-m', '--max-files', 'max_files', default=10, help='Specify How Match Files To Display')
def main_(path, max_files):
    fsize_list = get_dir_size(path, max_files)
    total_size = hurry.filesize.size(sum(fsize_list.values()))
    # this will return a list of tuple with value:key.
    size_sorted = sorted(zip(fsize_list.values(), fsize_list.keys()), reverse=True)

    print('[+] Total Size = {}'.format(total_size))
    print('[+] Top 10 File Size:')
    # TODO: This script does not calculate directory's size
    max_key = max(len(x[1]) for x in size_sorted)
    for key, value in size_sorted[:max_files]:
        print('    {:{max_key}} : {}'.format(value, hurry.filesize.size(key), max_key=max_key))


if __name__ == '__main__':
    main_()
