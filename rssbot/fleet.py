# This file is placed in the Public Domain.


"list of bots."


from .object import Object, values


rpr = object.__repr__


class Fleet(Object):

    "Fleet"

    def all(self):
        "return all objects."
        return values(self)

    def announce(self, txt):
        "announce on all bots."
        for bot in values(self):
            if "announce" in dir(bot):
                bot.announce(txt)

    def get(self, orig):
        "return bot."
        return getattr(self, orig, None)

    def register(self, obj):
        "add bot."
        setattr(self, rpr(obj), obj)


def __dir__():
    return (
        'Fleet',
    )
