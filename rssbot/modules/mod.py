# This file is placed in the Public Domain.


"available modules"


import os


def mod(event):
    "show available modules."
    path = os.path.dirname(__file__)
    mods = []
    for mdd in os.listdir(path):
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    event.reply(",".join(sorted(mods)))
