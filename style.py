_end   = '\x1b[0m'
_grey  = '\x1b[90m'
_red   = '\x1b[91m'
_green = '\x1b[92m'

# Runtime messages
def printm(m: str):
    print(f'{_grey}[{_green}+{_grey}]{_end} {m}')

# Runtime error
def printe(e: str):
    print(f'{_grey}[{_red}!{_grey}]{_end} {e}')

# Exceptions
def printx(x: Exception):
    print(f'{_grey}[{_red}!{_grey}] {type(x).__name__}{_end}: {str(x)}')
