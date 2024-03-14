# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"list of commands"


from ..handler import Client


def cmd(event):
    event.reply(",".join(sorted(list(Client.cmds))))


Client.add(cmd)