# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0612,E0402


"commands"


from rssbot.persist import Persist, find, last, sync
from rssbot.handler import Client


def cfg(event):
    config = Config()
    path = last(config)
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
        sync(config, path)
        event.reply('ok')


Client.add(cfg)

def cmd(event):
    event.reply(",".join(sorted(list(Client.cmds))))


Client.add(cmd)


def dpl(event):
    if len(event.args) < 2:
        event.reply('dpl <stringinurl> <item1,item2>')
        return
    setter = {'display_list': event.args[1]}
    for fnm, feed in find('rss', {'rss': event.args[0]}):
        if feed:
            update(feed, setter)
            sync(feed)
    event.reply('ok')


Client.add(dpl)


def mre(event):
    if not event.channel:
        event.reply('channel is not set.')
        return
    bot = Broker.get(event.orig)
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


Client.add(mre)


def nme(event):
    if len(event.args) != 2:
        event.reply('nme <stringinurl> <name>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector):
        if feed:
            feed.name = event.args[1]
            sync(feed)
    event.reply('ok')


Client.add(nme)


def pwd(event):
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


Client.add(pwd)


def rem(event):
    if len(event.args) != 1:
        event.reply('rem <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector):
        if feed:
            feed.__deleted__ = True
            sync(feed, fnm)
    event.reply('ok')


Client.add(rem)


def res(event):
    if len(event.args) != 1:
        event.reply('res <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector, deleted=True):
        if feed:
            feed.__deleted__ = False
            sync(feed, fnm)
    event.reply('ok')


Client.add(res)


def rss(event):
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
    for fnm, result in find('rss', {'rss': url}):
        if result:
            event.reply(f'already got {url}')
            return
    feed = Rss()
    feed.rss = event.args[0]
    sync(feed)
    event.reply('ok')


Client.add(rss)
