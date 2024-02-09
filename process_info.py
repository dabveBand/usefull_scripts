#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi@email.com
# created       : 18-Aug-2017
# updated       : 24-June-2022
#               : add cli_helper; and process by id; and process that has connections
#
# description   : get information about a process.
# dependencies  : psutil, cli_helpers, click
#
# ----------------------------------------------------------------------------

from datetime import datetime
import time
import os

import psutil
from cli_helpers import tabular_output
import click

import colors

color = colors.Colors()


def time_human(timestamp):
    """
    This will return a human time from timestamp
    args: timestamp
    return: date in hh:mm:ss
    """
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')


def table_display(data, headers, format_name='ascii'):
    """
    Display data as a table
    :data        : table data
    :headers     : table headers (description)
    :format_name : [ github | grid | vertical | ascii ]; default ascii
    """
    for row in tabular_output.format_output(data, headers, format_name=format_name):
        print(row)


def print_process_info(pid, p_info):
    """
    Print process informations in terminal
    :pid    : must be psutil.Process(process_id)
    :p_info : a dict object; ex: pid.as_dict(attrs=info_desc)
    """
    # iterate through the p_info dict
    print(color.title_msg('Process Information'))
    maxkey = max(len(key) for key in p_info.keys())          # for nice printing
    for key in sorted(p_info.keys()):
        print('    {:{maxkey}} : {}'.format(key.title(), p_info[key], maxkey=maxkey))

    parent = pid.parent()
    if parent:
        print('    {:<{maxkey}} : {} - {}'.format('Parent', parent.pid, parent.name(), maxkey=maxkey))

    parents = pid.parents()
    if parents:
        print('\n{}{} Parents{}'.format(color.replace['+'], color.BD, color.reset))
        headers = ['pid', 'Name', 'Status', 'Started']
        data = [[p.pid, p.name(), p.status(), time_human(p.create_time())] for p in parents]
        table_display(data, headers)

    childrens = pid.children(recursive=True)
    if childrens:
        print('\n{}{} Childrens{}'.format(color.replace['+'], color.BD, color.reset))
        headers = ['pid', 'Name', 'Status', 'Started']
        data = [[p.pid, p.name(), p.status(), time_human(p.create_time())] for p in childrens]
        table_display(data, headers)

    cmdline = pid.cmdline()
    if cmdline:
        print('\n{}{} Command Line{}'.format(color.replace['+'], color.BD, color.reset))
        print('    {}'.format(' '.join(cmdline)))

    try:
        conns = pid.connections()   # return a list of a namedtuples
    except psutil.AccessDenied:
        print(color.error_msg('Error: You must be root to see connections.'))
    else:
        if conns:
            # laddr = local address and port
            # raddr = remote address and port; can be empty if conn.status is listen (server)
            # for root process needs privileges
            print('\n{}{} Connections{}'.format(color.replace['+'], color.BD, color.reset))
            headers = ['family', 'from', 'to', 'status', 'type']
            data = [[con.family, '{}:{}'.format(con.laddr.ip, con.laddr.port), con.raddr, con.status, con.type] for con in conns]
            table_display(data, headers)


def process_info(process_id):
    """
    All Details for proccess by id
    work process_by_name
    :process_id: process id (pid) of the process
    """
    try:
        pid = psutil.Process(process_id)
    except PermissionError:
        print('Permission Error')
        exit()
    except psutil.NoSuchProcess:
        print(color.error_msg('Error: No such Process with pid: {}'.format(process_id)))
        exit()
    except psutil.AccessDenied:
        print(color.error_msg('You must be root'))
        exit()

    info_desc = ['cwd', 'name', 'exe', 'pid', 'status', 'username', 'terminal', 'memory_info', 'create_time']
    # get a list of valid attrs names
    # list(psutil.Process().as_dict().keys())
    p_info = pid.as_dict(attrs=info_desc)
    p_info['create_time'] = time_human(p_info['create_time'])   # change create_time to human readable time
    print_process_info(pid, p_info)

    input_msg = color.input_msg('do you want to terminate/suspend/resume :{}:{}: (t/s/r/Nothing): '.format(pid.pid, pid.name()))
    terminate = input(input_msg).lower()
    try:
        if terminate == 't':
            pid.terminate()
            print(color.info_msg('Terminated'))
        elif terminate == 's':
            pid.suspend()
            print(color.info_msg('Suspended'))
        elif terminate == 'r':
            pid.resume()
            print(color.info_msg('Resume'))
        else:
            pass
    except psutil.AccessDenied:
        print(color.error_msg('Error: This Process Belongs to {}'.format(p_info['username'].upper())))


def process_by_name(pname):
    # return a list of dict{'pid', 'name', 'status'}
    params = ['pid', 'name', 'status', 'connections']
    ps = [p.info for p in psutil.process_iter(attrs=params) if pname in p.info['name']]

    if len(ps) == 0:
        print(color.error_msg('No process found'))
    elif len(ps) > 1:
        print(color.info_msg('Found ({0}) Process With Name: ({1})\n'.format(len(ps), pname)))
        headers = ['Pid', 'Name', 'Status', 'Has Connections']
        data = list()
        for p in ps:
            lst = [p['pid'], p['name'], p['status']]
            if p['connections'] and len(p['connections']) > 0:
                lst.append('Yes')       # add has connections Yes.
            else:
                lst.append('')
            data.append(lst)
        table_display(data, headers)
        try:
            # get the pid of the process
            print()
            pidof = int(input(color.input_msg('Enter pid (0 for ALL): ')))
        except ValueError:
            print(color.error_msg('Exit: Value Error\n'))
        else:
            if pidof == 0:
                # display all process
                for index, p in enumerate(ps):
                    print('{2}{0}[ Process {1} ]{0}{3}'.format('=' * 30, index + 1, color.BD, color.reset))
                    process_info(int(p['pid']))
            else:
                process_info(pidof)
    else:
        # if one result in ps list
        ps = ps[0]
        process_info(ps['pid'])


def all_process():
    """
    Display All running process in a table
    """
    ps = [p.info for p in psutil.process_iter(['pid', 'name', 'username'])]
    headers = ps[0].keys()
    data = [p.values() for p in ps]
    table_display(data, headers)
    print('{}(=) Count {}{}'.format(color.BG, len(data), color.reset))


def process_by_username(username):
    """
    Display process for a given username in a table
    """
    # Get Process for user
    ps = [p.info for p in psutil.process_iter(['pid', 'name', 'username']) if username in p.info['username']]
    headers = ps[0].keys()
    data = [p.values() for p in ps]
    table_display(data, headers)
    print('{}(=) Count {}{}'.format(color.BG, len(data), color.reset))


def process_has_conn():
    """
    Process that has connections
    """
    ps = [int(conn.pid) for conn in psutil.net_connections() if conn.pid]
    pids = [psutil.Process(p) for p in ps]                                              # all pids as list of integers
    pids = [p for p in pids if p.name() != 'vim' and p.parent().name() != 'vim']        # without vim youCompleteMe

    print(color.info_msg('Found ({}) Process...'.format(len(pids))))
    time.sleep(2)

    for index, pid in enumerate(pids):
        info_desc = ['name', 'pid']
        p_info = pid.as_dict(attrs=info_desc)
        print_process_info(pid, p_info)
        print('{2}{0}[ Process {1} ]{0}{3}'.format('=' * 30, index + 1, color.BD, color.reset))


@click.command()
@click.option('-a', '--all-process', 'all_p', is_flag=True, default=False, help='All process.')
@click.option('--has-conn', 'has_conn', is_flag=True, default=False, help='Process that have connections.')
@click.option('-n', '--process-name', 'process_name', required=False, help='Process by name')
@click.option('-p', '--pid', 'pid', type=int, required=False, help='Process by ID')
@click.option('-u', '--username', 'username', required=False, help='Process for a given username')
def main(all_p, has_conn, process_name, pid, username):
    """
    Display Process Information By :

    [ username | process id |  process name | process that has connections ].
    """
    if all_p:
        all_process()
    elif username:
        process_by_username(username)
    elif process_name:
        os.system('cls' if os.name == 'nt' else 'clear')
        process_by_name(process_name)
    elif pid:
        os.system('cls' if os.name == 'nt' else 'clear')
        process_info(pid)
    elif has_conn:
        os.system('cls' if os.name == 'nt' else 'clear')
        process_has_conn()


if __name__ == '__main__':
    main()
    # process_has_conn()
    # process_info(23955)
