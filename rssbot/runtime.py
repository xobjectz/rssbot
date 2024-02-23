# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"main"


import getpass
import os
import sys
import time


from .clients import Client, cmnd
from .default import Default
from .excepts import Error, debug, enable
from .message import Message
from .parsers import parse_cmd
from .scanner import scan
from .utility import checkpid, daemon, forever, getpid, privileges
from .workdir import Workdir


from . import modules


Cfg         = Default()
Cfg.mod     = "cmd,irc,rss"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")


Workdir.wd = Cfg.wd


def main():
    parse_cmd(Cfg, " ".join(sys.argv[1:]))
    if checkpid(getpid(Cfg.pidfile)):
        return
    Cfg.mod = ",".join(modules.__dir__())
    Cfg.user = getpass.getuser()
    daemon(Cfg.pidfile, "v" in Cfg.opts)
    privileges(Cfg.user)
    scan(modules, Cfg.mod, True, Cfg.dis, True)
    forever()


if __name__ == "__main__":
    main()
