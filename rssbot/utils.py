# This file is placed in the Public Domain.


"utilities"


import uuid


def shortid():
    "create short id."
    return str(uuid.uuid4())[:8]


def skip(name, skipp):
    "check for skipping"
    for skp in spl(skipp):
        if skp in name:
            return True
    return False


def spl(txt):
    "split comma separated string into a list."
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def __dir__():
    return (
        'shortid',
        'skip',
        'spl'
    )
