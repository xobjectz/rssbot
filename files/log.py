# This file is placed in the Public Domain.
#
# pylint: disable=R,C,E0402


"log text"


import time


from rssbot.client  import laps
from rssbot.command import Command
from rssbot.object  import Object
from rssbot.find    import find, fntime
from rssbot.workdir import  sync
from rssbot.persist import whitelist


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


whitelist(Log)


def log(event):
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


Command.add(log)
