# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"show cached output"


from ..brokers import Broker


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
