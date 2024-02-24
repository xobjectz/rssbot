# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"runtime"


import getpass
import os
import sys


from .clients import cmnd 
from .default import Default
from .scanner import scan
from .utility import checkpid, daemon, forever, getpid, privileges
from .workdir import Workdir


from . import modules


Cfg         = Default()
Cfg.mod     = "cmd,irc,rss"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")
Cfg.user    = getpass.getuser()
Workdir.wd  = Cfg.wd


def cli():
    scan(modules, Cfg.mod)
    cmnd(" ".join(sys.argv[1:]), print)


def main():
    daemon(Cfg.pidfile)
    privileges(Cfg.user)
    scan(modules, Cfg.mod, True)
    forever()
