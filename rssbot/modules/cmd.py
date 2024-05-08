# This file is placed in the Public Domain.


"list of commands"



from ..client import Command


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(list(Command.cmds))))
