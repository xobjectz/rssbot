# This file is placed in the Public Domain.
# pylint: disable=R0903


"todo list"


import time


from ..cmds   import add
from ..object import Object
from ..disk   import find, sync, whitelist
from ..utils  import fntime, laps


class NoDate(Exception):

    "no matching date"


class Todo(Object):

    "Todo"

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


whitelist(Todo)


def dne(event):
    "flag todo as done."
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        sync(obj, fnm)
        event.reply('ok')
        break
    if not nmr:
        event.reply("nothing todo")


add(dne)


def tdo(event):
    "add todo."
    if not event.rest:
        nmr = 0
        for fnm, obj in find('todo'):
            lap = laps(time.time()-fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')


add(tdo)
