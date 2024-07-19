# This file is placed in the Public Domain.


"console"


from .client import Client
from .event  import Event
from .run    import fleet


class Console(Client):

    "Console"

    def __init__(self, outer, inner, prompt="> "):
        Client.__init__(self, outer)
        self.inner = inner
        self.prompt = prompt
        fleet.register(self)

    def announce(self, txt):
        "echo text"

    def callback(self, evt):
        "wait for callback."
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt = Event()
        evt.txt = self.inner(self.prompt)
        evt.type = "command"
        return evt
