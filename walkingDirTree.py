#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#          FILE: walkingDirTree.py
#         USAGE: ./walkingDirTree.py
#   DESCRIPTION: Walking a directory tree
#          From: Automate the boring stuff.pdf
#        AUTHOR: daBve (), dabve@outlook.fr
#       CREATED: 10-Sep-2017
# ----------------------------------------------------------------------------

import os


def walkDir(dir_name):
    if os.path.exists(dir_name):
        for folderName, subfolders, filenames in os.walk(dir_name):
            # current_folder = os.path.join()
            # print(folderName)

            for subfolder in subfolders:
                folder_name = os.path.join(folderName, subfolder)
                print('\t' + folder_name)

            for filename in filenames:
                file_name = os.path.join(folderName, filename)
                print(file_name)

            print('')
    else:
        print('\n[-] File does not exist\n')


if __name__ == '__main__':
    # import sys
    # if len(sys.argv) < 2:
    # dir_name = str(input('[:] Directory: '))
    walkDir('/home/dabve/python/bin')
    # else:
    # walkDir(sys.argv[1])
