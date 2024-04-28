# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"mailbox"


import mailbox
import os
import time


from ..object    import Object, fmt, update
from ..client    import laps
from ..find      import find, fntime
from ..whitelist import whitelist
from ..workdir   import sync


MONTH = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


class Email(Object):

    "Email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""


whitelist(Email)


def to_date(date):
    "match date in string." 
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], MONTH[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError) as ex:
        try:
            if "+" in res[4]:
                raise ValueError from ex
            if "-" in res[4]:
                raise ValueError from ex
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], MONTH[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], MONTH[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], MONTH[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], MONTH[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd


def cor(event):
    "correspondence"
    if not event.args:
        event.reply("cor <email>")
        return
    nr = -1
    for _fn, email in find("email", {"From": event.args[0]}):
        nr += 1
        txt = ""
        if len(event.args) > 1:
            txt = ",".join(event.args[1:])
        else:
            txt = "From,Subject"
        event.reply("%s %s %s" % (nr, fmt(email, txt, plain=True), laps(time.time() - fntime(email.__stp__))))


def eml(event):
    "emnail"
    if not event.args:
        event.reply("eml <searchtxtinemail>")
        return
    nr = -1
    for fn, o in find("email"):
        if event.rest in o.text:
            nr += 1
            event.reply("%s %s %s" % (nr, fmt(o, "From,Subject"), laps(time.time() - fntime(fn))))


def mbx(event):
    "mailbox"
    if not event.args:
        return
    fn = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        o = Email()
        update(o, m._headers) # pylint: disable=W0212
        o.text = ""
        for payload in m.walk():
            if payload.get_content_type() == 'text/plain':
                o.text += payload.get_payload()
        o.text = o.text.replace("\\n", "\n")
        sync(o)
        nr += 1
    if nr:
        event.reply("ok %s" % nr)
