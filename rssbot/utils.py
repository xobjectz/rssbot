# This file is placed in the Public Domain.
#
#


import sys


def getmain(name):
    main = sys.modules.get("__main__")
    return getattr(main, name, None)
