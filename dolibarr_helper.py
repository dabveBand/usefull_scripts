#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 11-August-2023
#
# description   : This script help interact with dolibarr database from python
# ----------------------------------------------------------------------------

import sys
from mysql.connector import connect, Error
import getpass

from rich.console import Console
from rich.table import Table
console = Console()


class MysqlFunc:
    """
    MySQL from python
    """
    def __init__(self, username, host='localhost', db_name=''):
        passwd = getpass.getpass(prompt='\n{}'.format('[:] Password: '))
        self.db_name = db_name

        self.config = {
            'user': username,
            'password': passwd,
            'host': host,
            'database': self.db_name
        }

    def login(self):
        """
        Login to a database
        """
        try:
            conn = connect(**self.config)
        except Error as err:
            console.print(f'[bold]([red]-[/red])[/bold] [red]Error[/red]: {err}')
            sys.exit()
        else:
            curs = conn.cursor()
        return conn, curs

    def make_query(self, query, params=()):
        """
        Make a query
        Args:
            query : 'Any query you want'
            params: params for the query
        return a tuple (description, curs.fetchall())
        """
        conn, curs = self.login()
        try:
            curs.execute(query, params)
        except Error as err:
            console.print(f'[b]([red]-[/red])[/b] [red]Error[/red]: {err}')
            sys.exit()
        else:
            starts_with = query.split()[0].lower()
            stmt = ['select', 'show', 'describe']
            if starts_with in stmt:
                desc = [desc[0] for desc in curs.description]
                rows = curs.fetchall()
                return (desc, rows)
            else:
                conn.commit()
                return '=> [{}] affected rows: {}'.format(query.split()[0].upper(), curs.rowcount)
        finally:
            if conn.is_connected():
                conn.close()

    def rich_table(self, table_title, descs, rows):
        """
        Display result in rich table
        Args:
            table_title: The title for table
            descs: table columns description from database
            rows: rows to display in table
        return a rich table
        """
        table = Table(title=table_title)
        for desc in descs:
            table.add_column(desc)
        for row in rows:
            row = map(str, row)
            table.add_row(*row)
        return table

    @property
    def show_databases(self):
        """
        Show databases
        """
        query = 'SHOW DATABASES'
        descs, rows = self.make_query(query)
        table = self.rich_table(query, descs, rows)
        console.print(table)

    @property
    def show_tables(self):
        """
        Show tables in a specific database
        """
        query = 'SHOW TABLES'
        descs, rows = self.make_query(query)
        table = self.rich_table(query, descs, rows)
        console.print(table)

    def describe_table(self, table_name):
        """
        Describing table(table_name)
        """
        query = 'DESCRIBE ' + table_name
        descs, rows = self.make_query(query)
        table = self.rich_table(query, descs, rows)
        console.print(table)


if __name__ == '__main__':
    user = 'dabve'
    host = 'localhost'
    db_name = 'dolibarr'
    # el3irbadth
    db_handler = MysqlFunc(user, host, db_name)
    # db_handler.show_databases
    # db_handler.show_tables
    db_handler.describe_table('llx_user')
    query = 'select login, pass from llx_user'
    desc, rows = db_handler.make_query(query)
    print(rows)
