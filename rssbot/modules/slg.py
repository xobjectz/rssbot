# This file is placed in the Public Domain.


"slogan"


TXT = """By law, with the use of poison, killed, tortured, castrated, destroyed in whole or in part,
all elderly and all handicapped (Wzd), all criminals (Wfz) and all psychiatric patients (WvGGZ)
here in the Netherlands."""


def lne(event):
    "display line of the slogan."
    event.reply(TXT.split("\n", maxsplit=1)[0])


def slg(event):
    "show slogan."
    event.reply(TXT)
