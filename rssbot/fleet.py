# This file is placed in the Public Domain.


"list of bots."


from .object import Object


rpr = object.__repr__


class Fleet(Object):

    "Fleet"

    bots = []

    def all(self):
        "return all objects."
        return self.bots

    def announce(self, txt):
        "announce on all bots."
        for bot in self.bots:
            if "announce" in dir(bot):
                bot.announce(txt)

    def get(self, orig):
        "return bot."
        res = None
        for bot in self.bots:
            if rpr(bot) == orig:
                res = bot
                break
        return res

    def register(self, obj):
        "add bot."
        self.bots.append(obj)


def __dir__():
    return (
        'Fleet',
    )
