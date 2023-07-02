#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 27-November-2022
#
# description   : From english to arabic
#                 Scrape "https://www.almaany.com/en/dict/ar-en" and then send data to `rich.table`
# usage         : en_ar_rich.py
# ----------------------------------------------------------------------------

from requests_html import HTMLSession
from rich.console import Console
from rich.table import Table

table = Table(title='Dict')
table.add_column('English', style='cyan')
table.add_column('Arabic', style='green')


def web_word():
    """
    Get the word from the internet
    :url: https://www.almaany.com/en/dict/ar-en/{word_to_translate}
    :return: rows for tuple(en, ar)
    """
    s = HTMLSession()
    word = input('[:] Enter word: ')
    r = s.get('https://www.almaany.com/en/dict/ar-en/{}'.format(word))

    html_panel = r.html.find('.panel-default .panel-body', first=True)
    records = list()        # to append dicts
    record = dict()         # build one element
    record['search_word'] = [elem.text for elem in html_panel.element.getchildren() if elem.tag == 'p']
    for elem in html_panel.element.getchildren():
        if elem.tag == 'p':
            record['word'] = elem.text
            print(elem.text)
        else:
            record['meaning'] = elem.find('b').text
            print(elem.find('b').text)
        records.append(record)
    print(records)

    # get examples
    html_tables = r.html.find('tbody')
    for tbl in html_tables:
        for tr in tbl.find('tr'):
            rows = [td.text for td in tr.find('td')[:2]]
            table.add_row(*rows)
    console = Console()
    console.print(table)
    return rows


if __name__ == '__main__':
    web_word()
