# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"messages"


import threading


from .brokers import Broker
from .default import Default


def __dir__():
    return (
        'Message',
   ) 


__all__ = __dir__()


class Message(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        bot = Broker.get(self.orig)
        for txt in self.result:
            bot.say(self.channel, txt)

    def wait(self):
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result
