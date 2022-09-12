#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =========================================
#  FILE     : sqlite_as_html.py
#  CREATED  : 29-juil.-2020
#  AUTHOR   : daBve, dabve@outlook.fr
#  DESC     : Send sqlite output to an html file.
#  USAGE    : ./sqlite_as_html.py
# =========================================

import sqlite3
from sqlite3 import Error


def boots_head(title):
    return """
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
""".format(title)


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


def login(db_name):
    """
    Connect to a specific database
    if database does not exist sqlite will create it
    """
    try:
        conn = sqlite3.connect(db_name)
    except Error as err:
        return err
    else:
        curs = conn.cursor()
        return conn, curs


def lst_tables_triggers(db_name, _type="trigger"):
    """
    List Tables OR Triggers and display it in bootstrap card:
        db_name : database name
        _type   : default triggers
    """
    conn, curs = login(db_name)
    query = 'SELECT name, sql FROM sqlite_master WHERE type = "' + _type + '"'
    try:
        curs.execute(query)
    except Error as err:
        print('[-] ERROR: {}'.format(err))
    else:
        rows = curs.fetchall()
        with open('table_trigger.html', 'w', encoding='utf8') as f:
            if _type == 'trigger':
                headers = boots_head('Triggers')
            elif _type == 'table':
                headers = boots_head('Tables')

            f.write(headers)         # Headers
            f.write('<div class="row">')

            # card for table names
            table_names = [row[0] for row in rows]
            f.write('<div class="col col-md-6"><div class="card mb-3">')
            f.write('<div class="card-header text-center">Table List</div>')       # card headers
            f.write('<div class="card-body">')
            f.write('<p class="card-text">{}</p></div></div></div>'.format("<br>".join(table_names)))

            for row in rows:
                f.write('<div class="col col-md-6"><div class="card mb-3">')
                f.write('<div class="card-header text-center">Name: {}</div>'.format(row[0]))       # card headers
                f.write('<div class="card-body">')
                for r in row[1:]:
                    # cart body
                    f.write('<p class="card-text">{}</p></div></div></div>'.format(r).replace("\n", "<br>"))

            f.write('</div>')
            f.write(footer)             # footer
    finally:
        if conn: conn.close()


def make_query(db_name, title, query, params=()):
    conn, curs = login(db_name)
    try:
        curs.execute(query, params)
    except Error as err:
        print('[-] ERROR: {}'.format(err))
    else:
        desc = [desc[0] for desc in curs.description]
        rows = curs.fetchall()
        with open('dump_records.html', 'w', encoding='utf-8') as f:
            headers = boots_head(title)
            f.write(headers)         # Headers

            # Table Head
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
            f.write(footer)             # footer
    finally:
        # close connection
        if conn: conn.close()


if __name__ == '__main__':
    # global vars
    db_name = '../../arabe/dbases/ar_en.sqlite'

    # list triggers or tables
    lst_tables_triggers(db_name, _type='table')

    # Make a query and display result in table
    table_name = 'WordsTable'
    title_page = 'Arabic To English'
    query = 'SELECT * FROM ' + table_name + ' ORDER BY id LIMIT 200'
    make_query(db_name, title_page, query)
