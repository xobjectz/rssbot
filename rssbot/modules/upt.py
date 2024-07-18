# This file is placed in the Public Domain.


"uptime"


import time


from ..cmds  import add
from ..utils import laps


STARTTIME = time.time()


def upt(event):
    "show uptime."
    event.reply(laps(time.time() - STARTTIME))


add(upt)
