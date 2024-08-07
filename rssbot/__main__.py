# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0212,W0613,E0401


"runtime"


import base64
import getpass
import os
import sys
import time


from rssbot.cfg    import Config
from rssbot.cmds   import Commands
from rssbot.dft    import Default
from rssbot.errors import errors
from rssbot.disk   import Persist, find, last, skel, sync
from rssbot.main   import cmnd, enable
from rssbot.object import construct, edit, fmt, keys, update
from rssbot.parse  import parse
from rssbot.run    import fleet
from rssbot.utils  import fntime, laps, privileges


from rssbot.modules.rss import DEBUG, TEMPLATE, Fetcher, OPMLParser, Rss
from rssbot.modules.rss import shortid


"config"


Cfg         = Config()
Cfg.dis     = ""
Cfg.mod     = "irc,rss"
Cfg.name    = "rssbot"
Cfg.opts    = ""
Cfg.user    = getpass.getuser()
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))


"irc"


def cfg(event):
    "configure command."
    config = Config()
    last(config)
    if not event.sets:
        event.reply(
                    fmt(
                        config,
                        keys(config),
                        skip='control,password,realname,sleep,username'.split(",")
                       )
                   )
    else:
        edit(config, event.sets)
        sync(config)
        event.reply('ok')


def mre(event):
    "show from output cache."
    if not event.channel:
        event.reply('channel is not set.')
        return
    bot = fleet.get(event.orig)
    if 'cache' not in dir(bot):
        event.reply('bot is missing cache')
        return
    if event.channel not in bot.cache:
        event.reply(f'no output in {event.channel} cache.')
        return
    for _x in range(3):
        txt = bot.gettxt(event.channel)
        if txt:
            bot.say(event.channel, txt)
    size = bot.size(event.channel)
    event.reply(f'{size} more in cache')


def pwd(event):
    "create a base64 password."
    if len(event.args) != 2:
        event.reply('pwd <nick> <password>')
        return
    arg1 = event.args[0]
    arg2 = event.args[1]
    txt = f'\x00{arg1}\x00{arg2}'
    enc = txt.encode('ascii')
    base = base64.b64encode(enc)
    dcd = base.decode('ascii')
    event.reply(dcd)


"rss"


def dpl(event):
    "set display items."
    if len(event.args) < 2:
        event.reply('dpl <stringinurl> <item1,item2>')
        return
    setter = {'display_list': event.args[1]}
    for fnm, feed in find("rss", {'rss': event.args[0]}):
        if feed:
            update(feed, setter)
            sync(feed, fnm)
    event.reply('ok')


def nme(event):
    "set name of feed."
    if len(event.args) != 2:
        event.reply('nme <stringinurl> <name>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find("rss", selector):
        if feed:
            feed.name = event.args[1]
            sync(feed, fnm)
    event.reply('ok')


def rem(event):
    "remove a feed."
    if len(event.args) != 1:
        event.reply('rem <stringinurl>')
        return
    for fnm, feed in find("rss"):
        if event.args[0] not in feed.rss:
            continue
        if feed:
            feed.__deleted__ = True
            sync(feed, fnm)
    event.reply('ok')


def res(event):
    "restore a feed."
    if len(event.args) != 1:
        event.reply('res <stringinurl>')
        return
    for fnm, feed in find("rss", deleted=True):
        if event.args[0] not in feed.rss:
            continue
        if feed:
            feed.__deleted__ = False
            sync(feed, fnm)
    event.reply('ok')


def rss(event):
    "add a feed."
    if not event.rest:
        nrs = 0
        for fnm, feed in find('rss'):
            nrs += 1
            elp = laps(time.time()-fntime(fnm))
            txt = fmt(feed)
            event.reply(f'{nrs} {txt} {elp}')
        if not nrs:
            event.reply('no rss feed found.')
        return
    url = event.args[0]
    if 'http' not in url:
        event.reply('i need an url')
        return
    for fnm, result in find("rss", {'rss': url}):
        if result:
            event.reply(f'already got {url}')
            return
    feed = Rss()
    feed.rss = event.args[0]
    sync(feed)
    event.reply('ok')


def syn(event):
    "synchronize feeds."
    if DEBUG:
        return
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run(True)
    nrs = 0
    for thr in thrs:
        thr.join()
        nrs += 1
    event.reply(f"{nrs} feeds synced")


"opml"


def exp(event):
    "export to opml."
    event.reply(TEMPLATE)
    nrs = 0
    for _fn, ooo in find("rss"):
        nrs += 1
        obj = Default()
        update(obj, ooo)
        name = obj.name or f"url{nrs}"
        txt = f'<outline name="{name}" display_list="{obj.display_list}" xmlUrl="{obj.rss}"/>'
        event.reply(" "*12 + txt)
    event.reply(" "*8 + "</outline>")
    event.reply("    <body>")
    event.reply("</opml>")


def imp(event):
    "import opml."
    if not event.args:
        event.reply("imp <filename>")
        return
    fnm = event.args[0]
    if not os.path.exists(fnm):
        event.reply(f"no {fnm} file found.")
        return
    with open(fnm, "r", encoding="utf-8") as file:
        txt = file.read()
    prs = OPMLParser()
    nrs = 0
    insertid = shortid()
    for obj in prs.parse(txt, 'outline', "name,display_list,xmlUrl"):
        feed = Rss()
        construct(feed, obj)
        feed.rss = obj.xmlUrl
        feed.insertid = insertid
        sync(feed)
        nrs += 1
    if nrs:
        event.reply(f"added {nrs} urls.")


"runtime"


def skl(event):
    "create service file (pipx)."
    privileges(getpass.getuser())
    skel()


def srv(event):
    "create service file (pipx)."
    if event.args:
        username = event.args[0]
    else:
        username  = getpass.getuser()
    txt = f"""[Unit]
Description={Cfg.name.upper()}
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
User={username}
Group={username}
ExecStartPre=/home/{username}/.local/bin/rssbot skl
ExecStart=/home/{username}/.local/bin/{Cfg.name}d
ExitType=cgroup
KillSignal=SIGKILL
KillMode=control-group
RemainAfterExit=yes
Restart=no

[Install]
WantedBy=default.target"""
    event.reply(txt)


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    enable(print)
    from rssbot import __main__
    Commands.scan(__main__)
    cmnd(Cfg.otxt, print)


"main"


if __name__ == "__main__":
    main()
    errors()
