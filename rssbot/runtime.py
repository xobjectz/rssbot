# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"main"


import getpass
import os
import readline
import sys
import time


from .clients import Client, cmnd
from .default import Default
from .excepts import Error, debug, enable
from .message import Message
from .parsers import parse_cmd
from .scanner import scan
from .utility import checkpid, daemon, forever, getpid, privileges, wrap
from .workdir import Workdir, skel


from . import modules


Cfg         = Default()
Cfg.mod     = "cmd,ena,mod"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")


Workdir.wd = Cfg.wd


class Console(Client):

    def announce(self, txt):
        pass

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Message()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def main():
    enable(print)
    skel()
    parse_cmd(Cfg, " ".join(sys.argv[1:]))
    readline.redisplay()
    if 'a' in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} {Cfg.opts.upper()} started {dte}")
    if "h" in Cfg.opts:
        from . import __doc__ as txt
        print(txt)
        return
    if "c" in Cfg.opts:
        scan(modules, Cfg.mod, True, Cfg.sets.dis, True)
        csl = Console()
        if 'z' in Cfg.opts:
            csl.threaded = False
        csl.start()
        forever()
        return
    if Cfg.otxt:
        Cfg.mod = ",".join(modules.__dir__())
        scan(modules, Cfg.mod, False, Cfg.sets.dis, False)
        return cmnd(Cfg.otxt, print)
    if checkpid(getpid(Cfg.pidfile)):
        print("daemon is already running.")
        return
    Cfg.mod = ",".join(modules.__dir__())
    Cfg.user = getpass.getuser()
    daemon(Cfg.pidfile, "v" in Cfg.opts)
    privileges(Cfg.user)
    scan(modules, Cfg.mod, True, Cfg.dis, True)
    forever()


def wrapped():
    wrap(main)
    Error.show()


if __name__ == "__main__":
    wrapped()
