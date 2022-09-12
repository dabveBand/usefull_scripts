#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /----------------------------------------------------------------------------
#          FILE: zipDetails.py
#         USAGE: ./zipDetails.py
#
#   DESCRIPTION: Getting infos from a zip file.
#
#          From: Automate the boring stuff.pdf
#        AUTHOR: daBve (), dabve@outlook.fr
#       CREATED: 10-Sep-2017
# \----------------------------------------------------------------------------

import zipfile, click


@click.command()
@click.option('-z', '--zip-file', required=True, help='Specify a ZIP file')
@click.option('-f', '--file-name', help='Specify a file name inside the zip')
def zipDetails(zip_file, file_name=None):
    zfile = zipfile.ZipFile(zip_file)
    with zipfile.ZipFile(zip_file) as zfile:
        list_name = zfile.namelist()    # list files in the zip file.
        for filename in list_name:
            print(filename)
        # Get info for sertin file from zip
        if file_name:
            print('\n[*] Details About: {}'.format(file_name))
            zinfo = zfile.getinfo(file_name)
            print('  File size: %s' % zinfo.file_size)
            print('  Compress size: %s' % zinfo.compress_size)


if __name__ == '__main__':
    zipDetails()
