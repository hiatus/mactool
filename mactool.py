#!/usr/bin/python3

import sys
import random
import argparse

import oui
from style import *

_banner = sys.argv[0].split('/')[-1].split('.')[0] + ''' \
[options] [arg]..
    -h, --help              this help
    -g, --generate          generate a random MAC address
    -u, --update            update OUI vendor database
    -v, --vendor    [str]   query database for the bytes of vendor string [str]
    -b, --bytes     [hex]   query database for the vendor string of bytes [hex]
    -s, --separator [char]  intersperse bytes with [char] (default: ':')

    Note: if -g is used along with -v or -b, the first bytes of the generated
    address will be set either to [hex] or bytes belonging to the vendor [str].
'''

def parse_args():
    parser = argparse.ArgumentParser(usage = _banner, add_help = False)

    parser.add_argument('-h', '--help', action = 'store_true')
    parser.add_argument('-g', '--generate', action = 'store_true')
    parser.add_argument('-u', '--update', action = 'store_true')
    parser.add_argument('-v', '--vendor', type = str, default = '')
    parser.add_argument('-b', '--bytes', type = str, default = '')
    parser.add_argument('-s', '--separator', type = str, default = ':')

    args = parser.parse_args()

    if args.vendor and not oui.is_vendor(args.vendor):
        raise ValueError(f'Invalid vendor string: {args.vendor}')

    args.bytes = args.bytes.replace(args.separator, '')

    if args.bytes:
        args.bytes = args.bytes.replace(args.separator, '')

        if not oui.is_bytes(args.bytes):
            raise ValueError(f'Invalid vendor bytes: {args.bytes}')

    return args


def main(args):
    if args.help:
        print(_banner, end = '')
        sys.exit(0)

    if args.update:
        printm('Updating vendor database')
        oui.update()
        sys.exit(0)

    if args.vendor:
        if not (vb := oui.vendor_bytes(args.vendor)):
            printe(f'Vendor not found: {args.vendor}')
            sys.exit(2)

        if args.generate:
            vb = random.choice(vb).upper()
            vb = f'{vb[:2]}{args.separator}{vb[2:4]}{args.separator}{vb[4:6]}'
        else:
            for b in vb:
                b = b.upper()
                print(f'{b[:2]}{args.separator}{b[2:4]}{args.separator}{b[4:6]}')

    elif args.bytes:
        if args.generate:
            vb = args.bytes.upper()
            vb = f'{vb[:2]}{args.separator}{vb[2:4]}{args.separator}{vb[4:6]}'

        elif not (bv := oui.bytes_vendor(args.bytes)):
            printe(f'Vendor bytes not found: {args.bytes}')
            sys.exit(2)

        else:
            print(bv)
    else:
        vb = args.separator.join([format(b, '02X') for b in random.randbytes(3)])

    if args.generate:
        db = args.separator.join([format(b, '02X') for b in random.randbytes(3)])
        print(f'{vb}{args.separator}{db}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(_banner, end = '')
        sys.exit(1)

    try:
        main(parse_args())

    except Exception as x:
        printx(x)
        sys.exit(1)
