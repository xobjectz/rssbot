# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"fleet"


from ..brokers import Broker
from ..utility import name


def flt(event):
    try:
        event.reply(Broker.all()[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in Broker.all()]))
