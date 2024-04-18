#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    :
# desc    : download file with requests
# ---------------------------------------------------------

import sys
import requests
from requests_html import HTML
from collections import namedtuple
from rich.console import Console

# FIXME
# this module is python/scripts/
# sys.extends
from service_status import service_st

console = Console()


def tor_session():
    ses = requests.Session()
    ses.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
    proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
    ses.proxies = proxies
    # url = 'http://httpbin.org/ip'
    return ses


def get_session(hider='tor'):
    """
    # make requests as a real browser
    # default with tor
    # tor is faster as hider
    """
    session = requests.session()
    if hider == 'tor':
        if service_st('tor'):
            session.proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
        else:
            print('(-) Error: you must enable Tor service in your machine.')
            sys.exit()
    elif hider == 'free':
        # NOTE: some hider use http only
        hider = get_hiders()[0]
        google_support = hider.google if hider.google != '' else 'No'
        print(console.print('using hider    : ' + hider.host))
        print(console.print('google support : ' + google_support))
        print(console.print('https  support : ' + hider.https))
        session.proxies = {'http': hider.host, 'https': hider.host}
    else:
        session.proxies = {}

    # chrom = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    # headers = {'Accept': 'application/json'}                                              # Accept json if site provide json
    # auth = HTTPBasicAuth('apikey', 'cqHfIqcYJGFYJzCGWoTgLI5CN5ocR11GD3uCGe1TLmm4I3Ea')    # Add apikey to HTTPBasicAuth

    ff = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'
    headers = {'User-Agent': ff}         # custom header for request; firefox headers
    session.headers = headers
    return session


def download_page(session, url, params=(), as_json=False):
    """
    :usage: download_page(session, url, params, as_json).
    :param: url    : params for the url.
    :param: params : params for the url.
    :param: as_json: return json data; else return text res
    """
    # referer == url add to headers to avoid 403 message
    # session.headers['referer'] = url
    try:
        res = session.get(url, params=params)
        res.raise_for_status()
    except Exception as err:
        print('[-] Err: {}'.format(err))
    else:
        if as_json: return res.json()           # json formated
        else: return res.text                   # as text


def post_data(session, url, payload, as_json=False):
    try:
        res = session.post(url, data=payload)
        res.raise_for_status()
    except Exception as err:
        print('[-] Err: {}'.format(err))
    else:
        if as_json: return res.json()           # json formated
        else: return res.text                   # as text


def save_tofile(data, file_of):
    with open(file_of, 'w') as f:
        f.write(data)
    print('[noun] done writing to: {}'.format(file_of))


def save_tojson(json_data, json_of):
    import json
    with open(json_of, 'w') as f:
        f.write(json.dumps(json_data, indent=2))
    print(console.print('done writing to: ' + json_of))


def tor_renew_connection():
    """
    # install tor as service
    # tor --hash-password 'password'
    # enable the Control port, and add a hashed password in /etc/tor/torrc
    """
    import getpass
    from stem.control import Controller
    from stem import Signal
    with Controller.from_port(port=9051) as c:
        passwd = getpass.getpass(prompt=console.input('tor password: '))
        c.authenticate(passwd)
        c.signal(Signal.NEWNYM)
        print(console.print('done NEWNYM.'))


def get_hiders():
    """
    get_hiders() from free-proxy-list
    return a list of namedtuple.
    """
    session = get_session()
    data = download_page(session, 'https://free-proxy-list.net/')
    html = HTML(html=data)

    tr = html.find('table > tbody > tr')
    hider = namedtuple('Hider', 'host google https country last_check')
    hiders_list = list()
    for data in tr[:20]:
        # return the first 20 hider
        try:
            ip, port, _, country, anonym, google, https, last_check = [d.text for d in data]
            host = '{}:{}'.format(ip, port)
            hiders_list.append(hider(host, google, https, country, last_check))
        except ValueError:
            pass

    return hiders_list


def hide_me():
    """
    # hide_me from hidemy.name
    # return a list of namedtuples object
    """
    s = get_session(hider=None)
    data = download_page(s, 'https://hidemy.name/en/proxy-list/')
    html = HTML(html=data)
    tbody = html.find('tbody tr')
    desc = ['ip', 'port', 'country', 'speed', 'type', 'anonym', 'latest_update']
    Hider = namedtuple('Hider', desc)
    try:
        lst = list(elem.text.split('\n') for elem in tbody)
    except ValueError:
        pass
    hiders = [Hider(*ls) for ls in lst]
    # anonym_proxy = [hider for hider in hide_me if hider.anonym != 'no']
    return hiders


if __name__ == '__main__':
    # make requests through tor
    ses = tor_session()
    url = 'https://www.httpbin.org/ip'
    res = ses.get(url)
    print(res.json())
    # Renew IP
    tor_renew_connection()
    res = ses.get(url)
    print(res.json())
    #
    # session = get_session()
    # data = download_page(session, url)
    # print(data)
