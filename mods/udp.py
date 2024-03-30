# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0105,E0402,R0903


"udp to irc relay"


import select
import socket
import sys
import threading
import time


from otpcr.broker import Broker
from otpcr.handler import Client
from otpcr.object import Object
from otpcr.thread import launch


def init():
    udpd = UDP()
    udpd.start()
    return udpd


class Cfg(Object):

    addr = ""
    host = "localhost"
    port = 5500


class UDP(Object):

    def __init__(self):
        Object.__init__(self)
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.ready = threading.Event()

    def output(self, txt, addr=None):
        if addr:
            Cfg.addr = addr
        for bot in Broker.all():
            bot.announce(txt.replace("\00", ""))

    def loop(self):
        try:
            self._sock.bind((Cfg.host, Cfg.port))
        except socket.gaierror:
            return
        self.ready.set()
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(
                          bytes("exit", "utf-8"),
                          (Cfg.host, Cfg.port)
                         )

    def start(self):
        launch(self.loop)


def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))


def udp(event):
    if event.rest:
        toudp(Cfg.host, Cfg.port, event.rest)
        event.reply(f"{len(event.rest)} characters sent")
        return
    if not select.select(
                         [sys.stdin, ],
                         [],
                         [],
                         0.0
                        )[0]:
        return
    size = 0
    while 1:
        try:
            (inp, _out, err) = select.select(
                                             [sys.stdin,],
                                             [],
                                             [sys.stderr,]
                                            )
        except KeyboardInterrupt:
            return
        if err:
            break
        stop = False
        for sock in inp:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            size += len(txt)
            toudp(Cfg.host, Cfg.port, txt)
        if stop:
            break


Client.add(udp)
