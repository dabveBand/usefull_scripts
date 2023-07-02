#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------
import os, sys
import typer
from rich.table import Table
from rich.console import Console
# ====== Global config var ====== #
clear = os.system('clear')
app = typer.Typer()
console = Console()
fname = './todo.txt'
if not os.path.exists(fname):
    os.system('touch todo.txt')


def error_msg(error_msg):
    console.print(f'\n\[[#c23616] Error [/]] {error_msg}\n', style='bold')


@app.command()
def show():
    """
    Show all todo files
    usage: todo.py show
    """
    clear
    lines = [line.strip() for line in open(fname)]          # all lines in a file

    table = Table(header_style='bold', title_justify='left')
    table.add_column('Number', justify='center', style='#1B9CFC')
    table.add_column('Todo', style='#00b894')
    for index, line in enumerate(lines, 1):
        table.add_row(str(index), line)
    console.print(table)
    console.print(f'\[[#487eb0] Counts [/]] {len(lines)} Todo.\n', style='bold')


@app.command()
def add(text: str = typer.Option(..., help='Todo text to add.')):
    """
    Add todo to the list.
    usage: todo.py add --text "some todo"
    """
    lines = [line.strip() for line in open(fname)]          # all lines in a file
    if len(lines) == 0:
        with open(fname, 'w') as f: f.write(text)
    else:
        with open(fname, 'a') as f: f.write('\n' + text)
    console.print('\n\[[#487eb0] Add [/]] Done adding todo.\n', style='bold')
    show()


@app.command()
def update(id: int = typer.Option(..., help='Todo id to update.'), text: str = typer.Option(..., help='Todo text.')):
    """
    Update todo with the given id and text
    usage: todo.py update --id 1 --text "update todo number 1"
    """
    lines = [line.strip() for line in open(fname)]          # all lines in a file
    if id > len(lines) or id == 0:
        show()
        error_msg(f'ID {id} does not exist.')
        sys.exit()
    with open(fname, 'w') as f:
        for index, line in enumerate(lines, 1):
            if index != id: f.write(line + '\n')
            else: f.write(text + '\n')
    console.print(f'\n\[[#487eb0] update [/]] Done updating todo with number {id}.\n', style='bold')
    show()


@app.command()
def remove(id: int = typer.Option(..., help='Specify the todo id to remove.')):
    """
    Delete todo with the given id
    usage: todo.py delete --id 1
    """
    lines = [line.strip() for line in open(fname)]          # all lines in a file
    if id > len(lines) or id == 0:
        show()
        error_msg(f'ID {id} does not exist.')
        sys.exit()
    with open(fname) as f:
        lines = [line.strip() for line in f]
    with open(fname, 'w') as f:
        for index, line in enumerate(lines, 1):
            if index != id:
                f.write(line)
    console.print(f'\n\[[#c23616] remove [/]] Done removing todo with number {id}.\n', style='bold')
    show()


if __name__ == '__main__':
    app()
