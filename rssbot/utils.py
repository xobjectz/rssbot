# This file is placed in the Public Domain.
#
#


"utilities"


import sys


def getmain(name):
    "fetch from __main__"
    main = sys.modules.get("__main__")
    return getattr(main, name, None)
