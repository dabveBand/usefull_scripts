#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 12-December-2022
#
# description   : Translate with google translate rapid api
# ----------------------------------------------------------------------------
import requests
import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command()
def translate(source: str = typer.Option('en', help='Source language to translate from.'),
              target: str = typer.Option('ar', help='Target language to translate to.'),
              text: str = typer.Option(..., help='Text to translate.')):
    """
    Translate with google translate rapid api
    NOTE: Problem encoding arabic latters if arabic in source
    """
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    payload = f"source={source}&target={target}&q={text}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "5348b9d3e4msh79e734953af7414p1f8f6ajsn7854424c1bb3",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    res = requests.request("POST", url, data=payload, headers=headers)
    translated_text = res.json()['data']['translations'][0]['translatedText']
    table = Table()
    table.add_column(source, justify='center', style='bold cyan')
    table.add_column(target, justify='center', style='bold green')
    table.add_row(text, translated_text)
    console.print(table)


if __name__ == '__main__':
    app()
