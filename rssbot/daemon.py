# This file is placed in the Public Domain.
# pylint: disable=C0411,C0413,W0212,W0718,E0401


"main"


import getpass
import os
import sys


from rssbot.cfg    import Config
from rssbot.disk   import Persist, skel
from rssbot.main   import init, wrap
from rssbot.utils  import forever, pidfile, privileges


from rssbot import modules


Cfg         = Config()
Cfg.mod     = "irc,rss"
Cfg.name    = "rssbot"
Cfg.user    = getpass.getuser()
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


def daemon(verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")


def main():
    "main"
    daemon()
    skel()
    privileges(Cfg.user)
    pidfile(Cfg.pidfile)
    init(Cfg.mod, modules)
    os.nice(10)
    forever()


if __name__ == "__main__":
    wrap(main)
