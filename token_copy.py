#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com

import click
import pyperclip
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


@click.command()
def list_values():
    """Command to list values from a given list"""
    keys = ['FIGMA_API', 'GITHUB', 'OPENAI_API', 'YOUTUBE_CHANNEL', 'GITHUB_LINK', ]
    click.echo('Values:')
    for value in keys:
        click.echo(f'- {value}')


@click.command()
@click.option('-l', '--list', 'lst', help='List of keys')
@click.argument('argument', required=False)
def get_value_from_dict(lst, argument):
    """
    This script takes an argument and copies the corresponding value from env variables to the clipboard.
    """
    # Check if the argument exists as an environment variable
    if lst:
        keys = ['FIGMA_API', 'GITHUB', 'OPENAI_API', 'YOUTUBE_CHANNEL', 'GITHUB_LINK', ]
        click.echo('Values:')
        for value in keys:
            click.echo(f'- {value}')

    if argument:
        argument = argument.upper()
        if argument in os.environ:
            value = os.environ[argument]
            pyperclip.copy(value)
            click.echo(f'{argument} Value copied to clipboard')
        else:
            click.echo('Key not found in environment variables.')


if __name__ == '__main__':
    get_value_from_dict()
