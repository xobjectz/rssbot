# This file is placed in the Public Domain.


"rest"


import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from ..default import Default
from ..errors  import debug, later
from ..find    import fns
from ..object  import Object
from ..thread  import launch
from ..workdir import Workdir


def init():
    "start object server."
    result = None
    try:
        result = REST((Config.hostname, int(Config.port)), RESTHandler)
    except OSError:
        pass
    if result:
        launch(result.start)
    return result


class Config(Default):

    "Config"

    hostname = "localhost"
    port     = 10102

    def __bla__(self):
        pass

    def __blabla__(self):
        pass


class REST(HTTPServer, Object):

    "REST"

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._last = time.time()
        self._starttime = time.time()
        self._status = "start"

    def exit(self):
        "shutdown server."
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self):
        "start server/"
        self._status = "ok"
        self.serve_forever()

    def request(self):
        "handler request."
        self._last = time.time()

    def error(self, request, addr):
        "handle error."
        exctype, excvalue, _tb = sys.exc_info()
        exc = exctype(excvalue)
        later(exc)
        if request:
            debug(f'{addr} {excvalue}')


class RESTHandler(BaseHTTPRequestHandler):

    "RESTHandler"

    def setup(self):
        "setup request."
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def send(self, txt):
        "send text."
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain'):
        "write a header."
        self.send_response(200)
        self.send_header('Content-type', f'{htype}; charset="utf-8"')
        self.send_header('Server', "1")
        self.end_headers()

    def do_GET(self): # pylint: disable=C0103
        "handle GET."
        if self.path == "/":
            self.write_header("text/html")
            txt = ""
            for fnm in fns():
                txt += f'<a href="http://{Config.hostname}:{Config.port}/{fnm}">{fnm}</a>\n'
            self.send(html(txt.strip()))
            return
        fnm = Workdir.workdir + os.sep + "store" + os.sep + self.path
        try:
            with open(fnm, "r", encoding="utf-8") as file:
                txt = file.read()
                self.write_header("txt/plain")
                self.send(html(txt))
        except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
            self.send_response(404)
            later(ex)
            self.end_headers()

    def log(self, code):
        "log access."
        debug(f"{self.address_string()} code {code} path {self.path}")


def html(txt):
    "html template."
    return f"<!doctype html><html>{txt}</html>"
