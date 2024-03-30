# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0612,W0613


"rest"


import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from otpcr.errors  import Errors, debug
from otpcr.object  import Default, Object
from otpcr.persist import Persist, Workdir
from otpcr.thread  import launch


def init():
    try:
        rest = REST((Config.hostname, int(Config.port)), RESTHandler)
    except OSError:
        return
    launch(rest.start)
    return rest


def html(txt):
    return """<!doctype html>
<html>
   %s
</html>
""" % txt


class Config(Default):

    hostname = "localhost"
    port     = 10102


class REST(HTTPServer, Object):

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
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self): 
        self._status = "ok"
        self.serve_forever()

    def request(self):
        self._last = time.time()

    def error(self, request, addr):
        exctype, excvalue, tb = sys.exc_info()
        exc = exctype(excvalue)
        Errors.add(exc)
        debug('%s %s' % (addr, excvalue))


class RESTHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def send(self, txt):
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain'):
        self.send_response(200)
        self.send_header('Content-type', '%s; charset=%s ' % (htype, "utf-8"))
        self.send_header('Server', "1")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.write_header("text/html")
            txt = ""
            for fnm in Persist.fns():
                txt += f'<a href="http://{Config.hostname}:{Config.port}/{fnm}">{fnm}</a>\n'
            self.send(html(txt.strip()))
            return
        fnm = Workdir.wd + os.sep + "store" + os.sep + self.path
        try:
            f = open(fnm, "r", encoding="utf-8")
            txt = f.read()
            f.close()
            self.write_header("txt/plain")
            self.send(html(txt))
        except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
            self.send_response(404)
            Errors.add(ex)
            self.end_headers()

    def log(self, code):
        debug('%s code %s path %s' % (self.address_string(), code, self.path))
