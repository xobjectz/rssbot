# This file is placed in the Public Domain.
# pylint: disable=W0125


"client"


from .cache  import Cache
from .cmds   import Commands
from .parse  import parse
from .react  import Reactor


class Client(Reactor):

    "Client"

    cache = Cache()
    out = None

    def __init__(self, outer=None):
        Reactor.__init__(self)
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


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Commands.cmds, evt.cmd, None)
    if func:
        func(evt)
        bot.show(evt)
    evt.ready()


def __dir__():
    return (
       'Client',
    )
