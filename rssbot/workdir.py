# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"working directory"


import os


from .objects import Object
from .utility import cdir


def __dir__():
    return (
        'Workdir',
        'skel',
        'store',
        'types'
    )


__all__ = __dir__()


class Workdir(Object):

    wd = ""


def skel():
    cdir(os.path.join(Workdir.wd, "store", ""))


def store(pth=""):
    return os.path.join(Workdir.wd, "store", pth)


def types():
    return os.listdir(store())
