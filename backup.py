#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =========================================
#  FILE     : check_path.py
#  CREATED  : 18-June-2020
#  AUTHOR   : daBve, dabve@outlook.fr
#  DESC     :
#  USAGE    :./check_path.py
# =========================================

# import os.path
import os
import shutil


def pause():
    """
    Pause terminal until ENTER is pressed
    title: Title of the pause function.from
    """
    try:
        print('Press <ENTER> ', end='')
        input()
    except KeyboardInterrupt:
        exit()


def building_copying(file2backup, src_path, dest_path):
    '''
    Building and copying new file from file2backup to destination path
        file2backup == List of files to backup.
        src_path    == To build the absolute path.
        dest_path   == Destination path
    USAGE: building_copying(file_to_backup, 'F:/backups/', 'D:/my_Folder/backups/')
    '''
    non_existing = list()                                       # non existing or commented lines
    for src in file2backup:
        # loop through source files
        src_f = os.path.join(src_path, src)                     # build the abspath   src_path/srcfile
        if os.path.exists(src_f):        # check if path exists and is a real path
            src_fname = os.path.abspath(src_f)                      # absolute path for the source file or directory
            dest_fname = dest_path + os.path.basename(src_fname)    # build destination path
            if os.path.isdir(src_fname):
                for folderName, subfolders, filenames in os.walk(src_fname):
                    # if path is a directory walk through all subdir and files.
                    src_dir = folderName                                        # source dir
                    dst_dir = dest_path + src_dir[len(src_path):]               # remove ('F:/backups/')
                    if os.path.exists(dst_dir) is False:
                        # if dir does not exist in dst_path
                        try:
                            print('[+] MKDIR: {}'.format(dst_dir))
                            os.mkdir(dst_dir)
                        except Exception as err:
                            print(err)

                    for filename in filenames:
                        src_filename = os.path.join(src_dir, filename)
                        dst_filename = dst_dir + '/' + filename
                        if os.path.exists(dst_filename):
                            if os.stat(src_filename).st_mtime - os.stat(dst_filename).st_mtime > 1:
                                # if src file is newer than dst file than copy.
                                if src_filename.endswith('pdf'):
                                    # skipping pdf files from updating
                                    pass
                                else:
                                    try:
                                        print('[+] UPDATE FILE: {}'.format(dst_filename))
                                        shutil.copy(src_filename, dst_filename)
                                    except Exception as err:
                                        print(err)
                        else:
                            try:
                                print('[+] NEW FILE: {}'.format(dst_filename))
                                shutil.copy(src_filename, dst_filename)
                            except Exception as err:
                                print(err)
            else:
                # if a file and not a dir
                try:
                    if os.stat(src_fname).st_mtime - os.stat(dest_fname).st_mtime > 1:
                        print('[+] UPDATE FILE: ', dest_fname)
                        shutil.copy(src_fname, dest_fname)
                except Exception as err:
                    print(err)
        else:
            non_existing.append(src_f)

    # print bad input in backup list.
    if non_existing:
        print('\n[-] Problem with:')
        for n_existing in non_existing:
            print(n_existing)


# remove files from backup dir, that are removed from source.
def remove_from_backup(dst_path, src_path):
    '''
    removing file that exists in SOURCE and not in DESTINATION.
        - dst_path: Dir to remove from.
        - src_path: Dir to check for existing of files.

    USAGE: remove_from_backup('D:/my_Folder/backups/', 'F:/backups/')         # remove file that exist on F:.. and not on D:..
    '''
    len_dst_path = len(dst_path)
    for folderName, subfolders, filenames in os.walk(dst_path):
        dst_dir = os.path.abspath(folderName)                     # Absolute path
        src_dir = src_path + dst_dir[len_dst_path:]               # removing the letters from dst_dir
        if os.path.exists(src_dir) is False:
            # if directory does not exist in source dir; then remove it
            print('[-] RM DIR: {}'.format(folderName))
            try:
                shutil.rmtree(folderName)
            except Exception as err:
                print(err)

        for filename in filenames:
            src_filename = os.path.join(src_dir, filename)
            dst_filename = os.path.join(folderName, filename)
            if os.path.exists(src_filename) is False:
                # if file does not exist in distination dir; then remove it
                print('[-] RM FILE: {}.'.format(dst_filename))
                try:
                    os.remove(dst_filename)
                except Exception as err:
                    print(err)


def main_menu():
    # Menu
    # TODO
    # create a menu
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
[+] Welcome to Backup Tool:

    1. LENEVO  -> USB
    2. USB     -> WINDOWS
    3. WINDOWS -> USB
    0. Exit.
    ''')
    choice = int(input('[:] Your Choice: '))
    return choice


if __name__ == '__main__':

    # Global var and PATH
    file_to_backup = ['python', 'bin', 'programming', '.cheat']         # list of file to backup.

    lenovo = '/home/dabve/'
    usb = '/media/dabve/dabve/backups/'
    usb_windows = 'F:/backups/'
    windows = 'D:/my_Folder/backups/'

    while True:
        choice = main_menu()
        if choice == 0:
            print('Exiting')
            break
        elif choice == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('[+] Lenovo to usb')
            building_copying(file_to_backup, lenovo, usb)
            remove_from_backup(usb, lenovo)
            pause()
        elif choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('[+] usb to windows')
            building_copying(file_to_backup, usb_windows, windows)
            remove_from_backup(windows, usb_windows)
            pause()
        elif choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('[+] windows to usb')
            building_copying(file_to_backup, windows, usb_windows)
            remove_from_backup(usb_windows, windows)
            pause()
