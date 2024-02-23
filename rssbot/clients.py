# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0613,E0402


"clients"


from .command import command 
from .handler import Handler
from .message import Message


def __dir__():
    return (
        'Client',
        'cmnd'
    )


__all__ = __dir__()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def show(self, evt):
        for txt in evt.result:
            self.say(evt.channel, txt)

    def raw(self, txt):
        pass


def cmnd(txt, out):
    clt = Client()
    clt.raw = out
    evn = Message()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    command(evn)
    evn.wait()
    return evn
