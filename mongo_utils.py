#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 19-December-2022
#
# description   : this file demonstrate how to use mongodb with python [reminder]
# --------------------------------------------------------------------------------
import pymongo
from pymongo import MongoClient
import typer
from rich.console import Console
from rich.table import Table
import hash_passwords

# =====| Config var |===== #
app = typer.Typer()                 # typer command line interface
console = Console()                 # nice printing
conn_str = '127.0.0.1'              # connection string
client = MongoClient(conn_str)      # mongodb client
users_db = client.users             # users database; if not exist; than create it
users_coll = users_db.users         # users collections; if not exist; than create it


# =====| DB Config |===== #
def users_schema():
    """Users schema like sql constraint"""
    users_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['username', 'password', 'email', 'fullname'],
            'properties': {
                'username': {'bsonType': 'string', 'description': 'must be a string and is required'},
                'password': {'bsonType': 'string', 'description': 'must be a string and is required'},
                'email': {'bsonType': 'string', 'description': 'must be a string and is required'},
                'fullname': {'bsonType': 'string', 'description': 'must be a string and is required'},
                'userGroupe': {'enum': ['Admin', 'Others'], 'description': 'user groupe must be Admin OR Other'},
            }
        }
    }
    users_db.command('collMod', 'users', validator=users_validator)             # create the validator
    users_coll.create_index([('username', pymongo.ASCENDING)], unique=True)     # unique constraint for username
# users_schema()


def success_msg(title, msg):
    console.print(f'\n\[ [#6495ed]{title}[/] ] {msg}', style='bold')


def danger_msg(title, msg):
    console.print(f'\n\[ [#b22222]{title}[/] ] {msg}', style='bold')


@app.command()
def add_user(username: str = typer.Option(..., '--name', '-u', help='Enter username.'),
             passwd: str = typer.Option(..., prompt='Enter password for new user', confirmation_prompt=True, hide_input=True),
             email: str = typer.Option(..., '--email', '-e', help='Enter email'),
             fullname: str = typer.Option(..., '--fullname', '-fname', help='Enter full name.'),
             user_groupe: str = typer.Option('Others', '--user-group', '-ug', help='User groupe Admin | Others default: Others')):
    """\bInsert new user to the database
    usage: ./mongo_utils.py add-user -u username -e user@email.com -fname 'user fullname' -ug Admin
    """
    pwd = hash_passwords.hash_password(passwd)
    user = {'username': username, 'password': pwd, 'email': email, 'fullname': fullname, 'userGroupe': user_groupe}
    try:
        inserted_id = users_coll.insert_one(user).inserted_id
    except pymongo.errors.DuplicateKeyError:
        danger_msg('Error', 'This username already exist')
    else:
        success_msg('Success', f'Inserted id {inserted_id}')


@app.command()
def user_info(username: str = typer.Option(..., '--username', '-u', help='Enter username.')):
    """\bSelect a specific user by username
    usage: ./mongo_utils.py user-info -u username
    """
    user = users_coll.find_one({'username': username})
    console.print(user)


@app.command()
def update_user(username: str = typer.Option(..., '--username', '-u', help='Enter username to update.'),
                new_username: str = typer.Option('', '--new-username', '-nu', help='Enter username'),
                new_email: str = typer.Option('', '--new-email', '-ne', help='Enter Email'),
                new_fullname: str = typer.Option('', '--new-fullname', '-nf', help='Enter fullname')):
    """\bUpdate a specific user by username
    usage: ./mongo_utils.py update-user -u username -nu new_username -ne new_email -nf new_fullname
    NOTE: not all fields are required you can omit some of them.
    """
    new_doc = dict()
    if new_username != '':
        new_doc['username'] = new_username
    elif new_email != '':
        new_doc['email'] = new_email
    elif new_fullname != '':
        new_doc['fullname'] = new_fullname

    result = users_coll.update_one({'username': username}, {'$set': new_doc})
    if result.raw_result['n'] > 0:
        success_msg('Success', f'done update {username}')
    else:
        danger_msg('Error', 'There was a problem. chack username and try again.')


@app.command()
def remove_user(username: str = typer.Option(..., '--username', '-u', help='Enter username to remove.')):
    """\bDelete a specific user by username
    usage: ./mongo_utils.py remove-user -u username
    """
    result = users_coll.delete_one({'username': username})
    if result.deleted_count > 0:
        danger_msg('Remove', 'Done removing user {username}')
    else:
        danger_msg('Error', 'There was a problem. chack username and try again.')


@app.command()
def change_password(
        username: str = typer.Option(..., '--username', '-u', help='Enter username to change password.'),
        passwd: str = typer.Option(..., prompt='Enter new password', confirmation_prompt=True, hide_input=True)):
    """\bChange password for a given username
    usage: ./mongo_utils.py change-password -u username
    """
    pwd = hash_passwords.hash_password(passwd)
    result = users_coll.update_one({'username': username}, {'$set': {'password': pwd}})
    if result.raw_result['n'] > 0:
        success_msg('Success', f'done update {username}')
    else:
        danger_msg('Error', 'There was a problem. chack username and try again.')


@app.command()
def list_users():
    """\bDisplay all users
    usage: ./mongo_utils.py list-users
    """
    # create the table instance with column name
    table = Table()
    table.add_column('_id')
    table.add_column('Username', style='bold cyan')
    table.add_column('Email', style='bold')
    table.add_column('Full Name', style='bold')
    table.add_column('User groupe', style='bold green')

    # get all records
    columns = {'username': 1, 'email': 1, 'fullname': 1, 'userGroupe': 1}
    users = users_coll.find({}, columns)
    for user in users:
        values = map(str, user.values())        # rich table row items must be string
        table.add_row(*values)                  # add values to the rich table
    console.print(table)
    users_count()
    print()


@app.command()
def users_count():
    """Count all users."""
    count = users_coll.estimated_document_count()
    success_msg('Count', f'{count} users.')


if __name__ == '__main__':
    app()
    # users_db.users.drop()                             # drop a collection
    # users_db = client['users']
    # coll = users_db['users']
    # dbs = client.list_database_names()                # list database names
    # print(dbs)
    # colls = users_db.list_collection_names()          # list all collections in a database
    # print(colls)
