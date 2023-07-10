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
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QLineEdit, QPushButton


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


def delete_note_from_database(note_id):
    """
    Delete a note from the database based on the provided note_id.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))

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


def create_note_dialog():
    """
    Create a PyQt5 dialog for adding notes.
    """
    app = QApplication([])
    app.setStyleSheet('''
* {
    background-color: #292929;
    color: #ffffff;
    font-family: Monaco;
}

QTextEdit, QPushButton {
    background-color: #424242;
    color: #ffffff;
}

QTextEdit::placeholder {
    color: #888888;
}
    ''')
    dialog = QDialog()
    dialog.setWindowTitle("Add Note")

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    # Description
    description_edit = QLineEdit()
    description_edit.setPlaceholderText('Enter Description')
    layout.addWidget(description_edit)

    # Content Text Edit
    content_edit = QTextEdit()
    content_edit.setPlaceholderText('Enter Your Note.')
    layout.addWidget(content_edit)

    save_button = QPushButton("Save")
    save_button.clicked.connect(
        lambda: save_dialog_note(
            content_edit.toPlainText(), description_edit.text(), dialog)
    )
    layout.addWidget(save_button)

    dialog.exec_()
    app.quit()


def save_dialog_note(content, description, dialog):
    """
    Save the note entered in the PyQt5 dialog.
    """
    save_note_to_database(content, description)
    click.echo("Note saved successfully!")
    dialog.close()


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
    table = Table(title="Notes", show_lines=True)
    table.add_column("ID", style="cyan", justify="left")
    table.add_column("Date", style='magenta', justify="left")
    table.add_column("Description")
    table.add_column("Content", style='green')

    notes = get_all_notes()

    for note in notes:
        id = str(note[0])
        date = note[1]
        # content_lines = note[2].split('\n')
        # content = '\n'.join(content_lines)
        content = note[2]
        desc = note[3]
        table.add_row(id, date, desc, content)

    console = Console()
    console.print(table, soft_wrap=True)


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


@click.command()
@click.argument("note_id", type=int)
def delete(note_id):
    """
    Delete a note.
    """
    delete_note_from_database(note_id)
    click.echo("Note deleted successfully!")


@click.command(name="add-gui")
def add_gui():
    """
    Add a new note using a GUI dialog.
    """
    create_note_dialog()


@click.group()
def cli():
    """
    Note app.
    """
    pass


cli.add_command(add)
cli.add_command(display)
cli.add_command(update)
cli.add_command(delete)
cli.add_command(add_gui)


if __name__ == "__main__":
    initialize_database()
    cli()
