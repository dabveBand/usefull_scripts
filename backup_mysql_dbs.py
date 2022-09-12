#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Desc     : Backup all MySQL databases, with all data in tables.
# Req      : subprocess, mysql_functions, click
# ---------------------------------------------------------------------------

from subprocess import Popen, PIPE
from mysql_functions import MysqlFunc
import click


@click.command()
@click.option('-u', '--user', metavar='MySQL username', prompt=True, required=True, help='User Name For MySQL Server.')
# @click.option('-f', '--file', 'out_file', metavar='<out file>', prompt=True, required=True, help='Out File to Write SQL Dump.')
def dump_dbases(user):
    """
    \b
    Dump all database from MySQL server and send output to file out
    NB: MysqlFunc handle the password.
    Usage:
        ./backup_mysql.py --user username --file out_file
    """
    db_handler = MysqlFunc(user)
    query = 'SHOW DATABASES'
    desc, rows = db_handler.make_query(query)
    ignore = ['sys', 'information_schema', 'performance_schema']
    for row in rows:
        db_name = row[0]
        if db_name in ignore:
            pass
        else:
            out_file = db_name + '_database.sql'
            with open(out_file, 'w') as f:
                try:
                    print('[+] DUMPING {}'.format(db_name.upper()))
                    p = Popen(['mysqldump', '-udabve', '-p', '--opt', db_name],
                              stdout=f,                     # stdout file out
                              stderr=PIPE,                  # stderr terminal
                              universal_newlines=True)      # new_lines
                except Exception as err:
                    print('[-] Error: {}'.format(err))
                else:
                    p.wait()                    # wait for the process
                    out, err = p.communicate()
                    if err:
                        print('[-] Error: {}'.format(err))
                    else:
                        print('\n[+] Done Dumping {}; File Name: {}\n'.format(db_name, out_file))


if __name__ == '__main__':
    dump_dbases()
