# This file is placed in the Public Domain.


"console"


from .cli   import CLI
from .event import Event


class Console(CLI):

    "Console"

    def __init__(self, outer, inner, prompt="> "):
        CLI.__init__(self, outer)
        self.inner = inner
        self.prompt = prompt

    def announce(self, txt):
        "disable announce."

    def callback(self, evt):
        "wait for callback."
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt = Event()
        evt.txt = self.inner(self.prompt)
        evt.type = "command"
        return evt
