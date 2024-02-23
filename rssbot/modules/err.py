# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0622,E0402


"status of bots"


from ..brokers import Broker
from ..excepts import Error


def err(event):
    nmr = 0
    for bot in Broker.all():
        if 'state' in dir(bot):
            event.reply(str(bot.state))
            nmr += 1
    event.reply(f"status: {nmr} errors: {len(Error.errors)}")
    for exc in Error.errors:
        txt = Error.format(exc)
        for line in txt.split():
            event.reply(line)
