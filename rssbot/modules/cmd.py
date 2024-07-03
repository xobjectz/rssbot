# This file is placed in the Public Domain.


"list of commands"


from ..cmds   import Commands, add
from ..object import keys


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.modnames))))


add(cmd)
