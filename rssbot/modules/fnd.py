# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0611,E0402


"locate"


from ..command import Command
from ..find    import find
from ..object  import fmt
from ..persist import long
from ..workdir import liststore, skel


def fnd(event):
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in liststore()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    if "." not in clz:
        for fnm in liststore():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")


#Command.add(fnd)