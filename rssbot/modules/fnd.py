# This file is placed in the Public Domain.


"locate"


from ..cmds   import add
from ..object import fmt
from ..disk   import find, long, skel, types


def fnd(event):
    "locate objects."
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in types()])
        if res:
            event.reply(",".join(res))
        return
    otype = long(event.args[0])
    nmr = 0
    for _fnm, obj in find(otype, event.gets):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")


add(fnd)
