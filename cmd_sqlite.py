#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# created  : 13-August-2020
# author   : el3arbi, el3arbi@email.com
# usage    : ./sqlite_cmd.py
#
# desc     : Manipulate sqlite database from cmd line
#            Do a simple task like:
#            - show databases
#            - show tables
#            - make a query
# req      : click, sqlite3
# NOTE     : this script is a reference on how to use command and options with click library
# -------------------------------------------------------------------------------------------

import click
import os

from sqlite_functions import SqliteFunc
import colors

color = colors.Colors()


@click.group(invoke_without_command=True)
@click.argument('db_name', metavar='<SQLite Database>', type=click.Path(exists=True))
@click.pass_context                             # pass context to sub command
def main(ctx, db_name):
    """
    \b
    A script to help:
        - show tables.
        - describe a table.
        - make a query.
    NB: for command help type: ./cmd_sqlite command --help
    """
    # ctx is the context to pass to subcommand.
    # here we pass the handler to subcommand
    handler = SqliteFunc(db_name)

    ctx.ensure_object(dict)                 # ensure that ctx.obj exists and is a dict
    ctx.obj['handler'] = handler            # add handler to ctx.obj dict
    os.system('cls' if os.name == 'nt' else 'clear')
    print(color.title_msg('Connected To: {}'.format(db_name)))


@main.command()
@click.pass_context
def show_tables(ctx):
    """
    Show Tables
    Usage: ./cmd_sqlite show-table db_name
    """
    # ctx contain the handler for the db.
    click.echo(color.simple_msg('List of Tables:'))
    click.echo()
    handler = ctx.obj['handler']                    # get the handler from ctx.obj dict
    handler.show_tables.table_display()             # show as table


@main.command()
@click.option('-t', '--table-name', 'tbl_name', metavar='<Table Name>', required=True, help='Table Name.')
@click.pass_context
def describe_table(ctx, tbl_name):
    """
    \b
    Describe Table
    Usage: ./cmd_sqlite describe-table db_name --table-name tbl_name
    """
    click.echo(color.simple_msg('Describe Table {}'.format(tbl_name)))
    click.echo()
    handler = ctx.obj['handler']                    # get the handler from ctx.obj dict
    handler.describe_table(tbl_name).vertical_display()


@main.command()
@click.option('-q', '--query', 'query', required=True, help='Make a CRUD Query.')
@click.option('-p', '--params', 'params', multiple=True, default=[], help='Parameters for the query.')
@click.option('-d', '--display', 'display', type=click.Choice(['table', 'vertical']), default='table', help='Display Format.')
@click.pass_context
def make_query(ctx, query, params, display):
    """
    \b
    Make a query
    Usage:
    ./cmd_sqlite db.sqlite make-query --query 'SELECT * FROM table_name WHERE id = 3'
    ./cmd_sqlite db.sqlite make-query -query 'SELECT * FROM table_name WHERE id = ?' --params 3
    ./cmd_sqlite db.sqlite make-query -q 'SELECT * FROM magasin_pdr WHERE designation = ? LIMIT ?' -p 'AXE' -p 5
    ./cmd_sqlite db.sqlite make-query -q 'SELECT * FROM magasin_pdr WHERE code LIKE ?' -p %aro% -d vertical
    """
    click.echo(color.simple_msg('{} | ? = {}'.format(query, params)))
    click.echo()
    handler = ctx.obj['handler']                     # get the handler from ctx.obj dict
    desc, rows = handler.make_query(query, params)   # make our query

    # how to display result: table | vertical
    if display == 'table':
        handler.display(desc, rows).table_display()
    elif display == 'vertical':
        handler.display(desc, rows).vertical_display()


if __name__ == '__main__':
    main()
