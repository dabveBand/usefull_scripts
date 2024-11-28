#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -------------------------------------
# FILE    : mysql_functions.py
# CREATED : 06-Apr-2019
# AUTHOR  : daBve, dabve@outlook.fr
#
# USAGE   : ./mysql_functions.py
#
# REQUIREMENT:
#
#   built-in: sys, csv, getpass, collections
#   third   : mysql.connector, terminaltables, cli_helpers, colorama
# -------------------------------------

import sys
import csv
import getpass

from mysql.connector import connect, Error
from sqlite_functions import Display

from rich.console import Console
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

    @property
    def show_databases(self):
        """
        Show databases
        Usage: show_databases(['table' | 'vertical' | 'namedtuple' | 'dict'])
        NB: if display is not given; then return a tuple (description, curs.fetchall())
        """
        query = 'SHOW DATABASES'
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    @property
    def show_tables(self):
        """
        Show tables in database
        Usage: show_tables(['table' | 'vertical' | 'namedtuple' | 'dict'])
        NB: if display is not given; then return a tuple (description, curs.fetchall())
        """
        query = 'SHOW TABLES'
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    @property
    def show_triggers(self):
        """
        Show Triggers
        Usage: show_triggers(['table' | 'vertical' | 'namedtuple' | 'dict'])
        NB: if display is not given; then return a tuple (description, curs.fetchall())
        """
        query = 'SHOW TRIGGERS'
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    def describe_table(self, table_name):
        """
        Describing table(table_name)
        NB: if display is not given; then return a tuple (description, curs.fetchall())
        """
        query = 'DESCRIBE ' + table_name
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    def make_query(self, query, params=()):
        """
        Make a query:
            query : 'Any query you want'
            params: params for the query
            return a tuple (description, curs.fetchall())
        """
        conn, curs = self.login()
        try:
            curs.execute(query, params)
        except Error as err:
            print('-' * 100)
            console.log(f'Error: {err}')
            print('-' * 100)
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

    def dump_records(self, table_name):
        """
        Dump all records in a given table name
        NB: if display is not given; then return a tuple (description, curs.fetchall())
        """
        query = 'SELECT * FROM ' + table_name
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    def display(self, desc, rows):
        """
        Display instance result is in sqlite_functions.py file:
        """
        display_inst = Display(desc, rows)
        return display_inst

    def save_to_html(self, out_file, page_title, query, params=()):
        """
        Save result of a query in an HTML file with bootstrap implementation
        Result in .\\mysql_bootstrap folder
            out_file    : Output file name.
            page_title  : The title of the web page.
            query       : any query you want.
            params      : query parameters
        """
        out_file = './mysql_bootstrap/' + out_file
        headers = """
                    <!doctype html>
                    <html lang="en">
                        <head>
                        <!-- Required meta tags -->
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                            <!-- Bootstrap CSS -->
                            <link rel="stylesheet" href="bootstrap.min.css">

                            <title>{0}</title>
                        </head>
                        <body>
                            <div class="containter">
                                <div class="col">
                                    <h1 class="text-center mb-5 mt-5">{0}</h1>
        """.format(page_title)
        footer = """
                            </div>
                        </div>

                        <!-- Optional JavaScript -->
                        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                        <script src="jquery-3.3.1.min.js"></script>
                        <script src="popper.min.js"></script>
                        <script src="bootstrap.min.js"></script>
                    </body>
                </html>
                """
        desc, rows = self.make_query(query, params)

        with open(out_file, 'w', encoding="utf8") as f:
            f.write(headers)
            f.write('''<p class="alert alert-success">QUERY: {} ---> "%s" = {}.
                       <br>RECORDS == {}.</p>'''.format(query, params, len(rows)))

            f.write('<table class="table table-bordered"><thead class="thead-dark"><tr>')
            for des in desc:
                # write table head description
                f.write('<th class="scope">{}</th>'.format(des.title()))        # lowercase first chars with .title()
            f.write('''</tr></thead>''')        # end of table headers
            # Table Body
            f.write('<tbody>')
            for row in rows:
                f.write('<tr>')
                for r in row:
                    f.write('<td>{}</td>'.format(r))
                f.write('</tr>')

            f.write('</tbody></table>')
            f.write(footer)
            print('\n=> done writing to HTML file: {}\n'.format(out_file))

    def load_csv(self, table_name, csv_file, headers=None):
        '''
        Load data from csv file to table_name
        :table_name: The table name to insert data on
        :csv_file: the csv file that contain records
        :headers: a list of column name in MySQL table

        You must:
            - Add headers to your file.
            - Values separated with ';'
        '''
        conn, curs = self.login()
        with open(csv_file, encoding='utf-8') as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')

            if not headers:
                headers = ', '.join(next(csv_reader))
            else:
                headers = ', '.join(headers)

            rows = [tuple(row) for row in csv_reader]
            bind = ('%s, ' * len(rows[0]))[:-2]              # bind will contain '?, ?' * headers number - the last', '

        query = 'INSERT INTO ' + table_name + '(' + headers + ') VALUES(' + bind + ')'
        try:
            curs.executemany(query, rows)
        except Error as err:
            console.log(f'Error: {err}')
        else:
            conn.commit()
            return '[+] {}: Rows Added Successfully'.format(curs.rowcount)
        finally:
            if conn.is_connected():
                conn.close()

    def save_to_csv(self, query, csv_out, delemiter=';'):
        """
        Save query result to csv file.
        """
        # conn, curs = self.login()
        desc, rows = self.make_query(query)
        with open(csv_out, 'w') as csv_f:
            csv_writer = csv.writer(csv_f, delimiter=delemiter)
            csv_writer.writerow(desc)       # write headers
            for row in rows:
                csv_writer.writerow(row)
        console.print(f'[bold]([blue]+[/blue])[/bold] Done writing to: {csv_out}')
        return True

    def __repr__(self):
        return '<__main__: {} connected to {!r} >'.format(self.__class__.__name__, self.db_name)


if __name__ == '__main__':
    # ----------------
    # => Config Var
    # ----------------
    user = 'dabve'
    host = 'localhost'
    db_name = 'eljoumou3a'
    db_handler = MysqlFunc(user, host, db_name)

    headers = ['id', 'harfText', 'hamimGroup', 'harfCountHamim', 'harfCountSuraName', 'harfQuranNumber', 'harfAbjad']
    result = db_handler.load_csv('harf_harf', './quraan_search_arabicharf.csv', headers=headers)
    print(result)

    # Query to create a database
    # query = 'create database if not exists stock_fact_idir character set "utf8"'
    # result = db_handler.make_query(query)
    # print(result)
    # print('#' * 50)
    #
    # ------------------
    # => show databases
    # ------------------
    # db_handler.show_databases.richtable_display

    # ---------------
    # => show tables
    # ---------------
    # db_handler.show_tables.richtable_display

    # ----------------
    # => show triggers
    # ----------------
    # db_handler.show_triggers.vertical_display()
    # rows = handler.show_triggers('dict')   # as named tuple

    # ---------------------
    # => describing tables
    # ---------------------
    # table_name = 'users'
    # db_handler.describe_table(table_name).vertical_display()

    # -------------------
    # => dump all records
    # -------------------
    # table_name = 'articles'
    # db_handler.dump_records(table_name).table_display()

    # --------------
    # => Reminder
    # --------------
    # query = 'SHOW GLOBAL STATUS LIKE Threads_connected'
    # query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = table_name'    # list of tables
    # Table column definition
    # query = '''SELECT COLUMN_NAME, ORDINAL_POSITION, COLUMN_DEFAULT, IS_NULLABLE, DATA_TYPE, COLUMN_TYPE, CHARACTER_SET_NAME
    #          # COLLATION_NAME, COLUMN_KEY FROM INFORMATION_SCHEMA.COLUMNS
    #          # WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s'''       # we can add: AND COLUMN_NAME = %s
    # params = ['Shop', 'articles']
    # desc, rows = db_handler.make_query(query, params)
    # db_handler.display(desc, rows).vertical_display()

    # as namedtuple
    # as_namedtuple = db_handler.display(desc, rows).as_namedtuple
    # for row in as_namedtuple:
        # print('fields  : ', row._fields)      # return fields
        # print('row     : ', row)
        # print('as dict : ', row._asdict())    # return OrderedDict

    # name that have blue color as color
    # user_name = {row.user_id: row.user_name for row in as_namedtuple if row.user_id == 1}
    # print(user_name)

    # name that have cats > 0 and cat not null
    # try:
        # users = {row.user_name: row.fname for row in as_namedtuple if row.reg_status == 1}
        # print(users)
    # except AttributeError as err:
        # err_msg = '[-] ERR: ' + str(err)
        # print(colors_.error_msg(err_msg))
        # print()
        # msg = '[+] choices are: ' + ' | '.join(desc)
        # print(colors_.simple_msg(msg))

    # -------------------------------
    # => save query to csv file
    # -------------------------------
    # csv_out = 'users_table.csv'
    # query = 'SELECT * FROM users'
    # rows = db_handler.save_to_csv(query, csv_out)
    # print(rows)

    # -------------------------------
    # => load csv file into database
    # -------------------------------
    # input_file = './users_table.csv'
    # rows = db_handler.load_csv('users', input_file)
    # print(rows)

    # -------------------------------
    # => save output to html file
    # -------------------------------
    # query = 'select * from users'
    # params = []
    # # query = 'SELECT * FROM magasin_pdr WHERE code LIKE %s LIMIT 10'
    # # params = ['%bhs%']
    # page_title = 'mysql users from our table'
    # out_file = 'index.html'
    # db_handler.save_to_html(out_file, page_title, query, params)

    # ----------------------------
    # => as a named tuples
    # ----------------------------
    # => MANIPULATE RESULT
