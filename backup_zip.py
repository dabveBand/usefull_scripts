#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File      : backup.py
# Usage     : ./backup.py
# Desc      : Create backup from config file
# Author    : daBve (), dabve@outlook.fr
# Created   : 03-Sep-2017
# ----------------------------------------------------------------------------

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
import click


def files_to_backup(configFile):
    # log_file = open('backup_zip.log', 'w')
    src_files = list(line.rstrip() for line in open(configFile))        # all path inside config file
    for f in src_files:
        for folderName, subfolders, filenames in os.walk(f):
            # for subfolder in subfolders:
            # folder_name = os.path.join(folderName, subfolder)
            # print('\t' + folder_name)

            for filename in filenames:
                file_name = os.path.join(folderName, filename)
                yield file_name
                print(file_name)
        # if os.path.exists(f) and os.path.abspath(f):                # if file exist and absolute path
            # # if os.path.isfile(f):
            # # print(os.path.abspath(f), file=log_file)
            # # # print(f, file=log_file)
            # # yield f                                             # Creating a generator.
            # # elif os.path.isdir(f):
            # # building directory recursively
            # for root, dirs, files in os.walk(f):
                # # for filename in files:
                # # filepath = os.path.join(root, filename)
                # # print(f, file=log_file)
                # # yield filepath

                # for subfolder in dirs:
                    # folder_name = os.path.join(root, subfolder)
                    # print('\t' + folder_name, file=log_file)
                    # yield folder_name

                # for filename in files:
                    # # print('\t' + folder_name)
                    # file_name = os.path.join(root, subfolder, filename)
                    # print('\t' + filename, file=log_file)
                    # yield file_name
        # else:
            # print('[-] missing file :: {}.'.format(f))
        # log_file.close()


@click.command()
@click.option('-c', '--config-file', 'configFile', required=True, help='Specify config file to backup from.')
@click.option('-d', '--dest', 'dest', default='.', help='Specify destination dir of backup file')
def backup(configFile, dest):
    """Building a ZIP file from config file."""
    if not os.path.exists(dest):
        print('\n=>Err: {} does not exist\n'.format(dest))
        exit()

    today = date.today()                                    # current data for the name of the zip
    zip_filename = 'main_backup_' + str(today) + '.zip'
    # removing old zip file with name 'backupImportatn*'
    for f in os.listdir(dest):
        if fnmatch(f, 'backupImportant*'):      # remove old version
            print('[+] Removing OLD ZIP file: {}'.format(zip_filename))
            os.remove(os.path.join(dest, f))

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        print('[+] creating the ZIP file {} ...'.format(zip_filename))
        for filename in files_to_backup(configFile):
            try:
                zipf.write(filename)
            except Exception as err:
                print(err)
        print('[+] done; archive in {}.'.format(dest))


if __name__ == '__main__':
    import os, zipfile
    from fnmatch import fnmatch
    from datetime import date

    backup()
