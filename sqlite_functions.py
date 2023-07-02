#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# created : 09-Apr-2019
# author  : daBve, dabve@gmail.fr
#
# description   : sqlite operations to help work with sqlite databases
# requirement   : sys, csv, collections(namedtuple, OrderedDict), sqlite3, terminaltables, xlsxwriter
# version       : from 1.0.0 to 1.1.0
# ---------------------------------------------------------------------------------------------


import pathlib, sys, csv
from collections import namedtuple, OrderedDict
import sqlite3
from sqlite3 import Error
from cli_helpers import tabular_output
from rich.console import Console

console = Console()


class MissingDbName(BaseException):
    def __str__(self):
        return 'You need to specify a database name'


class Display:
    def __init__(self, desc, rows):
        """
        Display result as:
        :desc: [desc[0] for desc in curs.description]
        :rows: curs.fetchall()
        (table | vertical | list of namedtuple object | list of dicts | list of an OrderedDict
        """
        self.desc = desc
        self.rows = rows

    @property
    def as_dict(self):
        """
        Return a list of OrderedDict
        >>> db_handler.make_query(query, display=True).as_dict
        """
        # return a list of dict objects
        rowdicts = [dict(zip(self.desc, row)) for row in self.rows]
        return rowdicts

    @property
    def as_orderedDict(self):
        """
        Return a list of OrderedDict
        >>> db_handler.make_query(query, display=True).as_orderedDict
        """
        # return a list of OrderedDict
        rowdicts = [OrderedDict(zip(self.desc, row)) for row in self.rows]
        return rowdicts

    @property
    def as_namedtuple(self):
        """
        Return a list of OrderedDict
        >>> db_handler.make_query(query, display=True).as_namedtuple
        """
        for ind, value in enumerate(self.desc):
            # namedtuple take this form: Parts = namedtuple('Parts', 'id_num desc cost amount')
            # find white space on fields_name and change it to '_' chars
            index = value.find(' ')     # index of white space inside value; find return the index
            if index > 0:
                self.desc[ind] = value.replace(' ', '_')
        Row = namedtuple('Row', self.desc)               # getting the key from description
        rows = [Row(*r) for r in self.rows]              # getting values
        return rows

    def table_display(self, display='grid', truncate_chars=False):
        """
        Display Result in Terminal with tabulate
        default display: 'grid'
        :display: [ascii, psql, grid, simple, html, csv, fancy_grid]
        """
        data, headers = self.rows, self.desc
        if truncate_chars:
            width = input('width of chars to truncate: ')
            data, headers = tabular_output.preprocessors.truncate_string(data, headers, max_field_width=width)   # truncate text

        for row in tabular_output.format_output(data, headers, format_name=display):
            print(row)
        console.print('\[[#17a2b8]counts[/]] {} Rows'.format(len(self.rows)), style='bold')

    @property
    def richtable_display(self):
        """
        Display result of query in terminal with rich.table
        """
        from rich.table import Table
        table = Table(header_style='bold magenta')
        for desc in self.desc: table.add_column(desc)
        for row in self.rows:
            row = map(str, row)
            table.add_row(*row)
        console.print(table)
        console.print('\[[#17a2b8]Counts[/]]: {} Rows'.format(len(self.rows)), style='bold')


class SqliteFunc:
    def __init__(self, db_name):
        if pathlib.Path(db_name).is_file() and pathlib.Path(db_name).exists():
            self.db_name = db_name
        else:
            self.error_msg(81, 'DB with name {} does not exits.'.format(db_name))
            create = input('do you want to create it [y/N]: ')
            if create.lower() in ('y', 'yes'):
                self.db_name = db_name
            else:
                sys.exit()

    def error_msg(self, lineno, err):
        console.print('[bold]\[[#dc3545]error[/]] line {}: {}[/]'.format(lineno, err))

    def success_msg(self, msg):
        console.print('[bold]\[[#17a2b8]success[/]] {}[/]'.format(msg))

    def login(self):
        """
        login to database; if database does not exist; than create it
        """
        try:
            conn = sqlite3.connect(self.db_name)
        except Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            self.error_msg(exc_lineno, err)
        else:
            conn.execute('PRAGMA foreign_keys = 1')
            curs = conn.cursor()
            return conn, curs

    @property
    def show_tables(self):
        """
        Show All Tables in database
        return a display instance
        """
        query = 'SELECT name FROM sqlite_master WHERE type = "table"'
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    def describe_table(self, table_name):
        """
        Describe a table
        :table_name: the table name
        :return: a display instance
        >>> db_handler.describe_table('table_name')
        """
        query = 'SELECT * FROM sqlite_master WHERE type ="table" and name = ?'
        desc, rows = self.make_query(query, [table_name])
        return self.display(desc, rows)

    def show_idx_trigg_view(self, type_of):
        """
        usage: show_idx_trigg_view('index | triggers | view')
        :return: display instance
        """
        # select * from sqlite_master where type = 'index'      # to show indexes
        # select * from sqlite_master where type = 'view'       # to show views
        query = 'SELECT * FROM sqlite_master WHERE type = ?'
        desc, rows = self.make_query(query, [type_of])
        return self.display(desc, rows)

    def make_query(self, query, params=(), display=False):
        """
        usage : make_query('select * from table_name where id = ?', [1])
        return: tuple(desc, rows) | rowcount for update and delete operations
        """
        conn, curs = self.login()
        try:
            curs.execute(query, params)
        except Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            self.error_msg(exc_lineno, err)
            sys.exit()
        else:
            stmt = query.split()[0].upper()
            if stmt == 'SELECT':
                desc = [desc[0] for desc in curs.description]
                rows = curs.fetchall()
                if display:
                    return self.display(desc, rows)
                else:
                    return (desc, rows)
            else:
                conn.commit()
                return '[{}]: {} affected rows.'.format(stmt, curs.rowcount)
        finally:
            if conn: conn.close()

    def create_tables(self, table_name, fields):
        """
        usage : create_tables('table_name', ['id INTEGER', 'add_date DATETIME'])
        return: result from sqlite3
        """
        query = 'CREATE TABLE {}(\n{}\n)'.format(table_name, ',\n'.join(fields))
        return self.make_query(query)

    def create_index(self, index_name, table_name, field):
        """
        create_index('idx_code_article', 'table_name', 'id')
        return the result from sqlite3
        """
        query = 'CREATE INDEX {} ON {}({})'.format(index_name, table_name, field)
        return self.make_query(query)

    def create_trigger(self, trigger_name, operation, table_name, stmt):
        """
        usage: create_trigger('update_value', 'AFTER UPDATE', 'table_name', 'update table_name set value = qte * value')
        NB   : you must now how to create a trigger in SQL
        """
        query = '''CREATE TRIGGER {} {} ON {}
                   BEGIN
                       {};
                   END'''.format(trigger_name, operation, table_name, stmt)
        return self.make_query(query)

    def dump_records(self, table_name):
        """
        usage: dump_records(table_name)
        Return a display instance
        """
        query = 'SELECT * FROM ' + table_name
        desc, rows = self.make_query(query)
        return self.display(desc, rows)

    def product_exists(self, table, column, value):
        """
        usage : product_exists('magasin', 'reference', 'product_reference')
        return True or False
        """
        conn, curs = self.login()
        try:
            curs.execute('SELECT id FROM ' + table + ' WHERE ' + column + ' = ?', [value])
        except Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            self.error_msg(exc_lineno, err)
        else:
            if curs.fetchone(): return True
            else: return False
        finally:
            if conn: conn.close()

    def display(self, desc, rows):
        display_inst = Display(desc, rows)
        return display_inst

    def write_to_csv(self, csv_out, query, params=()):
        """
        Write a query to a csv file
            usage   : write_to_csv('outfile.csv', 'SELECT * FROM table WHERE id = ?', [10])
            csv_out : Out file to write into
            query   : SQL Query
            params  : parameters for the query
        """
        conn, curs = self.login()
        desc, rows = self.make_query(query, params)
        with open(csv_out, 'w', encoding='utf-8') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(desc)
            count = 0
            for row in rows:
                csv_writer.writerow(row)
                count += 1
        self.success_msg('done writing [#20c997]{}[/] Rows to [#20c997]{}[/].'.format(count, csv_out))

    def write_to_html(self, out_file, page_title, query, params=()):
        """
        Desc : write a query to an html file with bootstrap templetes.
        Usage: write_to_html(out_file, page_title, query, params)
            out_file    : output file name; out dir sqlite_bootstrap
            page_title  : title of the web page
            query       : you query
            params      : params for the query
        """
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
        out_file = './sqlite_bootstrap/' + out_file
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
            self.success_msg('done writing to <style fg="#20c997">{}</style>'.format(out_file))

    def load_from_csv(self, table_name, csv_file, sep=';'):
        '''
        Load data from csv file to table_name
        :NOTE       : Add headers to your file.
        :table_name : Table Name
        :csv_file   : Input CSV File
        :sep        : Fields Separator(delimiter) Default ';'
        '''
        conn, curs = self.login()
        # with open(csv_file, encoding='latin-1') as input_file:
        with open(csv_file, encoding='utf-8') as input_file:
            csv_reader = csv.reader(input_file, delimiter=sep)
            headers = ', '.join(next(csv_reader))               # string that containt headers to add to the query
            rows = [tuple(row) for row in csv_reader]
            bind = ('?, ' * len(rows[0]))[:-2]                  # bind will contain '?, ?' * headers number

        query = 'INSERT INTO ' + table_name + '(' + headers + ') VALUES(' + bind + ')'
        try:
            curs.executemany(query, rows)
        except Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            self.error_msg(exc_lineno, err)
        else:
            conn.commit()
            self.success_msg('{} loaded rows to [#20c997]{}[/].'.format(curs.rowcount, table_name))
        finally:
            if conn: conn.close()

    def write_to_excel(self, excel_fname, query, params=()):
        import xlsxwriter
        from datetime import datetime
        today = datetime.today()
        with xlsxwriter.Workbook(excel_fname) as wbook:
            wsheet = wbook.add_worksheet()

            desc_format = wbook.add_format({'font_name': 'Times New Roman',
                                            'bold': True,
                                            'font_size': 16,
                                            'border': 1,
                                            'align': 'center',
                                            'valign': 'center'})
            rows_format = wbook.add_format({'font_name': 'Times New Roman', 'font_size': 14, 'border': 1})
            date_format = wbook.add_format({'num_format': 'dd mmmm yyyy'})
            wsheet.write(0, 5, 'Date: ' + today.strftime('%d %m %Y'), date_format)

            desc, rows = self.make_query(query, params)
            excel_row = 1
            excel_col = 0
            for des in desc:
                # write description
                wsheet.write(excel_row, excel_col, des, desc_format)
                excel_col += 1

            excel_row = 1
            for row in rows:
                excel_col = 0
                for r in row:
                    wsheet.write(excel_row, excel_col, r, rows_format)
                    excel_col += 1
                excel_row += 1
        self.success_msg('done writing to <style fg="#20c997">{}</style>'.format(excel_fname))
        return '(+) Done Writing to: {}'.format(excel_fname)

    def __repr__(self):
        return '<{!r} connected to {!r} >'.format(self.__class__.__name__, self.db_name)

# ------------------ End of Class


def atache_database(curs, dbname, alias):
    """
    # When you have multiple databases available and you want to use any one of them at a time.
    # SQLite ATTACH DATABASE statement is used to select a particular database,
      and after this command, all SQLite statements will be executed under the attached database.
    """
    query = 'ATTACH DATABASE ' + dbname + ' AS ' + alias
    curs.execute(query)


if __name__ == '__main__':
    db_name = '../django_app/arab_english/english_arabic/db.sqlite3'
    db_handler = SqliteFunc(db_name)

    # db_handler.show_tables.table_display()                   # terminal_default
    table_name = 'translator_arenqamos'
    query = f'select * from {table_name}'
    db_handler.write_to_csv('arab_english.csv', query, params=())
    # db_handler.load_from_csv(table_name, './arab_english.csv', sep=';')
