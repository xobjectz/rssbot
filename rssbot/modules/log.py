# This file is placed in the Public Domain.


"log text"


import time


from ..client import laps
from ..disk   import sync
from ..find   import find, fntime
from ..object import Object


class Log(Object): # pylint: disable=R0903

    "Log"

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    "log text."
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            lap = laps(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')
