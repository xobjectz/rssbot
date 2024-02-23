# This file is placed in the Public Domain.
#
# pylint: disable=C,R


import sys


from .clients import cmnd
from .default import Default
from .runtime import Cfg
from .scanner import scan


from . import modules


Cfg.mod = ",".join(modules.__dir__())


def main():
    scan(modules, Cfg.mod)
    cmnd(" ".join(sys.argv[1:]), print)


if __name__ == "__main__":
    main()