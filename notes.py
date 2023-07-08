#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 08-July-2023
#
# description   : create note and display with rich.tables
# ----------------------------------------------------------------------------

import click
import sqlite3
from datetime import datetime
from rich.table import Table
from rich.console import Console

DB_NAME = "notes.db"


def initialize_database():
    """
    Initialize the SQLite database and create the 'notes' table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the notes table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        description TEXT NOT NULL
        )"""
    )

    conn.commit()
    conn.close()


def save_note_to_database(content, description):
    """
    Save a new note to the database.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (date, content, description) VALUES (?, ?, ?)",
        (now, content, description),
    )

    conn.commit()
    conn.close()


def update_note_in_database(note_id, content, description):
    """
    Update an existing note in the database based on the provided note_id.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content = ?, description = ? WHERE id = ?",
        (content, description, note_id),
    )

    conn.commit()
    conn.close()


def get_all_notes():
    """
    Retrieve all notes from the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    conn.close()

    return notes


@click.command()
@click.argument("content")
@click.option("-d", "--description", prompt="Enter a description", help="Add a description for the note")
def add(content, description):
    """
    Save a new note.
    """
    save_note_to_database(content, description)
    click.echo("Note saved successfully!")


@click.command()
def display():
    """
    Display all notes.
    """
    table = Table(title="Notes")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Date")
    table.add_column("Content")
    table.add_column("Description")

    notes = get_all_notes()

    for note in notes:
        table.add_row(str(note[0]), note[1], note[2], note[3])

    console = Console()
    console.print(table)


@click.command()
@click.argument("note_id", type=int)
@click.argument("content")
@click.option("-d", "--description", prompt="Enter a new description", help="Add a new description for the note")
def update(note_id, content, description):
    """
    Update an existing note.
    """
    update_note_in_database(note_id, content, description)
    click.echo("Note updated successfully!")


@click.group()
def cli():
    """
    Note app.
    """
    pass


cli.add_command(add)
cli.add_command(display)
cli.add_command(update)


if __name__ == "__main__":
    initialize_database()
    cli()
