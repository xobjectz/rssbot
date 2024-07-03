# This file is placed in the Public Domain.
# pylint: disable=W0125


"command line interface"


from .cmds   import command
from .handle import Handler
from .object import Object


class CLI(Handler):

    "CLI"

    cache = Object()
    out = None

    def __init__(self, outer=None):
        Handler.__init__(self)
        self.register("command", command)
        self.out = outer

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        if self.out:
            txt = txt.encode('utf-8', 'replace').decode()
            self.out(txt)

    def show(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)


def __dir__():
    return (
       'CLI',
    )
