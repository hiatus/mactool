#!/usr/bin/python3

import re
import requests

from os import path

_oui_fs = ':'
_oui_remote = 'http://standards-oui.ieee.org/oui/oui.txt'
_oui_local = f'{path.dirname(path.abspath(__file__))}/res/oui.txt'

_oui_re_bytes  = re.compile('^[a-fA-F0-9]{6,12}$')
_oui_re_vendor = re.compile('^[a-zA-Z_,\.\-\ \(\)]+$')

is_bytes  = lambda b: True if _oui_re_bytes.match(b)  else False
is_vendor = lambda v: True if _oui_re_vendor.match(v) else False

def update():
    if (r := requests.get(_oui_remote)).status_code != 200:
        raise RuntimeException('Failed to retrieve remote OUI information')

    with open(_oui_local, 'w') as dst:
        for l in r.text.split('\n'):
            if '(hex)' in l:
                l = l.split()

                dst.write(
                    f"{l[0].replace('-', '').upper()}"
                    f"{_oui_fs}{' '.join(l[2:])}\n"
                )

def vendor_bytes(v: str) -> tuple:
    vb = []
    v = v.lower()

    with open(_oui_local, 'r') as src:
        for l in src:
            if v in l.lower():
                vb.append(l.split(_oui_fs)[0])

    return tuple(vb)


def bytes_vendor(b: str) -> str:
    b = b.upper()[:4]

    with open(_oui_local, 'r') as src:
        for l in src:
            if b in l:
                return l.strip().split(_oui_fs)[1]

    return ''
