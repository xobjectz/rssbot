# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"locate"


from objx import Storage, find, fmt


def fnd(event):
    Storage.skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Storage.types()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = Storage.long(otype)
    if "." not in clz:
        for fnm in Storage.types():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
