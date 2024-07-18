# This file is placed in the Public Domain.


"available modules"


import os


from .. import user


def mod(event):
    "show available modules."
    path = os.path.dirname(__file__)
    mods = []
    for mdd in os.scandir(path):
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    path = os.path.dirname(user.__file__)
    for mdd in os.scandir(path):
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    event.reply(",".join(sorted(mods)))
