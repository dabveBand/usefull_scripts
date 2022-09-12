#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------

from sqlite_functions import SqliteFunc
import click


@click.command()
@click.option('-w', '--word', 'word', required=True, help='Word to Translate to Arabic Language')
def translate(word):
    db_handler = SqliteFunc('../arabic_dbases/ar_en.sqlite')
    query = 'SELECT word, meaning FROM WordsTable WHERE searchword LIKE ?'
    params = ['%' + word + '%']
    desc, rows = db_handler.make_query(query, params)
    db_handler.display(desc, rows).terminal_display()


if __name__ == '__main__':
    translate()
