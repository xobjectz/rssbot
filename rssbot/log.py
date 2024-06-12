# This file is placed in the Public Domain.


"logging"


class Logging: # pylint: disable=R0903

    "Logging"

    filter = []
    out    = None


def debug(txt):
    "print to console."
    for skp in Logging.filter:
        if skp in txt:
            return
    if Logging.out:
        Logging.out(txt) # pylint: disable=E1102


def __dir__():
    return (
        'Logging',
        'debug'
    )
