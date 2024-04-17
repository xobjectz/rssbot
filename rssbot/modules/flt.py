# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"fleet"


from ..command import Command
from ..object  import values
from ..runtime import broker
from ..thread  import name


def flt(event):
    bots = values(broker.objs)
    try:
        event.reply(bots[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))


Command.add(flt)
