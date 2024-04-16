# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"list of commands"


from ..command import Command


def cmd(event):
    event.reply(",".join(sorted(list(Command.cmds))))


Command.add(cmd)