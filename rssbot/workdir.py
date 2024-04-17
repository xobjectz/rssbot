# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"working directory"


import datetime
import os


from .object import Object, cdir, fqn, read, write


class Workdir(Object):

    "Workdir"

    workdir = ""


def fetch(obj, pth):
    "read object from disk."
    pth2 = store(pth)
    read(obj, pth2)
    return strip(pth)


def ident(obj):
    "return an id for an object."
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def liststore():
    "return types stored."
    return os.listdir(store())


def skel():
    "create directory,"
    cdir(os.path.join(Workdir.workdir, "store", ""))


def store(pth=""):
    "return objects directory."
    return os.path.join(Workdir.workdir, "store", pth)


def strip(pth, nmr=3):
    "reduce to path with directory."
    return os.sep.join(pth.split(os.sep)[-nmr:])


def sync(obj, pth=None):
    "sync object to disk."
    if pth is None:
        pth = ident(obj)
    pth2 = store(pth)
    write(obj, pth2)
    return pth
