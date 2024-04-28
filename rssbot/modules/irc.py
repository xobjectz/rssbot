# This file is placed in the Public Domain.


"internet relay chat"


import base64
import os
import queue
import socket
import ssl
import textwrap
import threading
import time
import _thread


from ..client    import Client, command
from ..default   import Default
from ..event     import Event
from ..errors    import Errors, debug, later
from ..find      import last
from ..object    import Object, edit, fmt, keys, values
from ..runtime   import broker
from ..thread    import launch
from ..whitelist import whitelist
from ..workdir   import sync


NAME    = __file__.split(os.sep)[-3]
saylock = _thread.allocate_lock()


Errors.filter = ["PING", "PONG", "PRIVMSG"]


def init():
    "initialize a irc bot."
    irc = IRC()
    irc.start()
    irc.events.joined.wait()
    return irc


def shutdown():
    "shutdown irc bot."
    for bot in values(broker.objs):
        if "irc" not in str(type(bot)).lower():
            continue
        debug(f"IRC stopping {repr(bot)}")
        bot.state.pongcheck = True
        bot.state.keeprunning = False
        bot.events.connected.clear()
        bot.stop()


class Config(Default): # pylint: disable=R0902,R0903

    "Config"

    channel = f'#{NAME}'
    commands = False
    control = '!'
    edited = time.time()
    nick = NAME
    port = 6667
    realname = NAME
    sasl = False
    server = 'localhost'
    servermodes = ''
    sleep = 60
    username = NAME
    users = False
    verbose = False

    def __init__(self):
        Default.__init__(self)
        self.channel = self.channel or Config.channel
        self.commands = self.commands or Config.commands
        self.nick = self.nick or Config.nick
        self.port = self.port or Config.port
        self.realname = self.realname or Config.realname
        self.server = self.server or Config.server
        self.username = self.username or Config.username


whitelist(Config)


class TextWrap(textwrap.TextWrapper):

    "TextWrap"

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 400


wrapper = TextWrap()


class Output():

    "Output"

    cache = Object()

    def __init__(self):
        self.dostop = threading.Event()
        self.oqueue = queue.Queue()

    def dosay(self, channel, txt):
        "overload this."
        raise NotImplementedError

    @staticmethod
    def extend(channel, txtlist):
        "add list of txt to channel cache."
        if channel not in Output.cache:
            Output.cache[channel] = []
        chanlist = getattr(Output.cache, channel)
        chanlist.extend(txtlist)

    @staticmethod
    def gettxt(channel):
        "return text from channel cache."
        txt = None
        try:
            che = getattr(Output.cache, channel, None)
            if che:
                txt = che.pop(0)
        except (KeyError, IndexError):
            pass
        return txt

    def oput(self, channel, txt):
        "put text to output queue."
        if channel and channel not in dir(Output.cache):
            setattr(Output.cache, channel, [])
        self.oqueue.put_nowait((channel, txt))

    def out(self):
        "output loop."
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                break
            if self.dostop.is_set():
                break
            txtlist = wrapper.wrap(txt)
            if len(txtlist) > 3:
                self.extend(channel, txtlist)
                length = len(txtlist)
                self.say(
                         channel,
                         f"use !mre to show more (+{length})"
                        )
                continue
            _nr = -1
            for txt in txtlist:
                _nr += 1
                self.dosay(channel, txt)

    @staticmethod
    def size(chan):
        "return size of channel cache."
        if chan in Output.cache:
            return len(getattr(Output.cache, chan, []))
        return 0


class IRC(Client, Output):

    "IRC"

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)
        self.buffer = []
        self.cfg = Config()
        self.channels = []
        self.events = Default()
        self.events.authed = threading.Event()
        self.events.connected = threading.Event()
        self.events.joined = threading.Event()
        self.events.ready = threading.Event()
        self.sock = None
        self.state = Default()
        self.state.dostop = False
        self.state.error = ""
        self.state.keeprunning = False
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrsend = 0
        self.zelf = ''
        self.register('903', cb_h903)
        self.register('904', cb_h903)
        self.register('AUTHENTICATE', cb_auth)
        self.register('CAP', cb_cap)
        self.register('ERROR', cb_error)
        self.register('LOG', cb_log)
        self.register('NOTICE', cb_notice)
        self.register('PRIVMSG', cb_privmsg)
        self.register('QUIT', cb_quit)
        self.register("366", cb_ready)
        broker.add(self)

    def announce(self, txt):
        "announce on all channels."
        for channel in self.channels:
            self.oput(channel, txt)

    def docommand(self, cmd, *args):
        "send command to server."
        with saylock:
            if not args:
                self.raw(cmd)
            elif len(args) == 1:
                self.raw(f'{cmd.upper()} {args[0]}')
            elif len(args) == 2:
                txt = ' '.join(args[1:])
                self.raw(f'{cmd.upper()} {args[0]} :{txt}')
            elif len(args) >= 3:
                txt = ' '.join(args[2:])
                self.raw("{cmd.upper()} {args[0]} {args[1]} :{txt}")
            if (time.time() - self.state.last) < 5.0:
                time.sleep(5.0)
            self.state.last = time.time()

    def connect(self, server, port=6667):
        "connect to server."
        self.state.nrconnect += 1
        self.events.connected.clear()
        if self.cfg.password:
            debug("using SASL")
            self.cfg.sasl = True
            self.cfg.port = "6697"
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
            ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ctx.wrap_socket(sock)
            self.sock.connect((server, port))
            self.direct('CAP LS 302')
        else:
            addr = socket.getaddrinfo(server, port, socket.AF_INET)[-1][-1]
            self.sock = socket.create_connection(addr)
            self.events.authed.set()
        if self.sock:
            os.set_inheritable(self.sock.fileno(), os.O_RDWR)
            self.sock.setblocking(True)
            self.sock.settimeout(180.0)
            self.events.connected.set()
            return True
        return False

    def direct(self, txt):
        "send text directly on the socket."
        with saylock:
            self.raw(txt)
            time.sleep(2.0)

    def disconnect(self):
        "disconnect from server."
        try:
            self.sock.shutdown(2)
        except (
                ssl.SSLError,
                OSError,
                BrokenPipeError
               ) as _ex:
            pass
        except Exception as ex: # pylint: disable=W0718
            later(ex)

    def doconnect(self, server, nck, port=6667):
        "loop until connected."
        while 1:
            try:
                if self.connect(server, port):
                    break
            except (
                    ssl.SSLError,
                    OSError,
                    ConnectionResetError
                   ) as ex:
                self.state.error = str(ex)
                debug(str(ex))
            debug(f"sleeping {self.cfg.sleep} seconds")
            time.sleep(self.cfg.sleep)
        self.logon(server, nck)

    def event(self, txt):
        "create an event."
        evt = self.parsing(txt)
        cmd = evt.command
        if cmd == 'PING':
            self.state.pongcheck = True
            self.docommand('PONG', evt.txt or '')
        elif cmd == 'PONG':
            self.state.pongcheck = False
        if cmd == '001':
            self.state.needconnect = False
            if self.cfg.servermodes:
                self.docommand(f'MODE {self.cfg.nick} {self.cfg.servermodes}')
            self.zelf = evt.args[-1]
        elif cmd == "376":
            self.joinall()
        elif cmd == '002':
            self.state.host = evt.args[2][:-1]
        elif cmd == '366':
            self.state.error = ""
            self.events.joined.set()
        elif cmd == '433':
            self.state.error = txt
            nck = self.cfg.nick + '_'
            self.docommand('NICK', nck)
        return evt

    def joinall(self):
        "join all channels."
        for channel in self.channels:
            self.docommand('JOIN', channel)

    def keep(self):
        "keep alive."
        while not self.stopped.is_set():
            if self.state.stopkeep:
                self.state.stopkeep = False
                break
            self.events.connected.wait()
            self.events.authed.wait()
            self.state.keeprunning = True
            time.sleep(self.cfg.sleep)
            self.state.pongcheck = True
            self.docommand('PING', self.cfg.server)
            if self.state.pongcheck:
                debug("failed pongcheck, restarting")
                self.state.pongcheck = False
                self.state.keeprunning = False
                self.events.connected.clear()
                self.stop()
                init()
                break

    def logon(self, server, nck):
        "log onto server,"
        self.events.connected.wait()
        self.events.authed.wait()
        self.direct(f'NICK {nck}')
        self.direct(f'USER {nck} {server} {server} {nck}')


    def parsing(self, txt):
        "parse text into an event."
        # pylint: disable=R0912,R0915
        rawstr = str(txt)
        rawstr = rawstr.replace('\u0001', '')
        rawstr = rawstr.replace('\001', '')
        debug(txt)
        obj = Event()
        obj.args = []
        obj.rawstr = rawstr
        obj.command = ''
        obj.arguments = []
        arguments = rawstr.split()
        if arguments:
            obj.origin = arguments[0]
        else:
            obj.origin = self.cfg.server
        if obj.origin.startswith(':'):
            obj.origin = obj.origin[1:]
            if len(arguments) > 1:
                obj.command = arguments[1]
                obj.type = obj.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(':') <= 1 and arg.startswith(':'):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        obj.arguments.append(arg)
                obj.txt = ' '.join(txtlist)
        else:
            obj.command = obj.origin
            obj.origin = self.cfg.server
        try:
            obj.nick, obj.origin = obj.origin.split('!')
        except ValueError:
            obj.nick = ''
        target = ''
        if obj.arguments:
            target = obj.arguments[0]
        if target.startswith('#'):
            obj.channel = target
        else:
            obj.channel = obj.nick
        if not obj.txt:
            obj.txt = rawstr.split(':', 2)[-1]
        if not obj.txt and len(arguments) == 1:
            obj.txt = arguments[1]
        spl = obj.txt.split()
        if len(spl) > 1:
            obj.args = spl[1:]
        if obj.args:
            obj.rest = " ".join(obj.args)
        obj.orig = object.__repr__(self)
        obj.txt = obj.txt.strip()
        obj.type = obj.command
        return obj

    def poll(self):
        "poll for event."
        self.events.connected.wait()
        if not self.buffer:
            try:
                self.some()
            except BlockingIOError as ex:
                time.sleep(1.0)
                return self.event(str(ex))
            except (
                    OSError,
                    socket.timeout,
                    ssl.SSLError,
                    ssl.SSLZeroReturnError,
                    ConnectionResetError,
                    BrokenPipeError
                   ) as ex:
                later(ex)
                self.stop()
                debug("handler stopped")
                evt = self.event(str(ex))
                return evt
        try:
            txt = self.buffer.pop(0)
        except IndexError:
            txt = ""
        return self.event(txt)

    def raw(self, txt):
        "send raw text."
        txt = txt.rstrip()
        debug(txt)
        txt = txt[:500]
        txt += '\r\n'
        txt = bytes(txt, 'utf-8')
        if self.sock:
            try:
                self.sock.send(txt)
            except (
                    OSError,
                    ssl.SSLError,
                    ssl.SSLZeroReturnError,
                    ConnectionResetError,
                    BrokenPipeError
                   ) as ex:
                later(ex)
                self.stop()
                return
        self.state.last = time.time()
        self.state.nrsend += 1

    def reconnect(self):
        "reconnect to server."
        debug(f"reconnecting to {self.cfg.server}")
        try:
            self.disconnect()
        except (ssl.SSLError, OSError):
            pass
        self.events.connected.clear()
        self.events.joined.clear()
        self.doconnect(self.cfg.server, self.cfg.nick, int(self.cfg.port))

    def dosay(self, channel, txt):
        "method for output cache."
        self.events.joined.wait()
        txt = str(txt).replace('\n', '')
        txt = txt.replace('  ', ' ')
        self.docommand('PRIVMSG', channel, txt)

    def say(self, channel, txt):
        "say text on channel."
        self.oput(channel, txt)

    def some(self):
        "parse part of input text."
        self.events.connected.wait()
        if not self.sock:
            return
        inbytes = self.sock.recv(512)
        txt = str(inbytes, 'utf-8')
        if txt == '':
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split('\r\n')
        for line in splitted[:-1]:
            self.buffer.append(line)
        self.state.lastline = splitted[-1]

    def start(self):
        "start bot."
        last(self.cfg)
        if self.cfg.channel not in self.channels:
            self.channels.append(self.cfg.channel)
        self.events.connected.clear()
        self.events.joined.clear()
        launch(Output.out, self)
        launch(Client.start, self)
        launch(
               self.doconnect,
               self.cfg.server or "localhost",
               self.cfg.nick,
               int(self.cfg.port or '6667')
              )
        if not self.state.keeprunning:
            launch(self.keep)

    def stop(self):
        "stop bot."
        self.state.stopkeep = True
        self.disconnect()
        self.dostop.set()
        self.oput(None, None)
        Client.stop(self)

    def wait(self):
        "wait for ready."
        self.events.ready.wait()


def cb_auth(bot, evt):
    "auth callback."
    bot.docommand(f'AUTHENTICATE {bot.cfg.password}')


def cb_cap(bot, evt):
    "capabilities callback."
    if bot.cfg.password and 'ACK' in evt.arguments:
        bot.direct('AUTHENTICATE PLAIN')
    else:
        bot.direct('CAP REQ :sasl')


def cb_error(bot, evt):
    "error callback."
    if not bot.state.nrerror:
        bot.state.nrerror = 0
    bot.state.nrerror += 1
    bot.state.error = evt.txt
    debug(evt.txt)


def cb_h903(bot, evt):
    "auth succeded callback."
    bot.direct('CAP END')
    bot.events.authed.set()


def cb_h904(bot, evt):
    "auth succeded callback."
    bot.direct('CAP END')
    bot.events.authed.set()


def cb_kill(bot, evt):
    "got killed callback."


def cb_log(bot, evt):
    "log callback."


def cb_ready(bot, evt):
    "bot is ready callback."
    bot.events.ready.set()


def cb_001(bot, evt):
    "first line received callback."
    bot.logon()


def cb_notice(bot, evt):
    "notice callback."
    if evt.txt.startswith('VERSION'):
        txt = f'\001VERSION {NAME.upper()} 140 - {bot.cfg.username}\001'
        bot.docommand('NOTICE', evt.channel, txt)


def cb_privmsg(bot, evt):
    "privmsg callback."
    if not bot.cfg.commands:
        return
    if evt.txt:
        if evt.txt[0] in ['!',]:
            evt.txt = evt.txt[1:]
        elif evt.txt.startswith(f'{bot.cfg.nick}:'):
            evt.txt = evt.txt[len(bot.cfg.nick)+1:]
        else:
            return
        if evt.txt:
            evt.txt = evt.txt[0].lower() + evt.txt[1:]
        debug(f"command from {evt.origin}: {evt.txt}")
        command(bot, evt)


def cb_quit(bot, evt):
    "quit callback."
    debug(f"quit from {bot.cfg.server}")
    if evt.orig and evt.orig in bot.zelf:
        bot.stop()


def cfg(event):
    "configure command."
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


def mre(event):
    "show from output cache."
    if not event.channel:
        event.reply('channel is not set.')
        return
    bot = broker.get(event.orig)
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
