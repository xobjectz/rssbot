# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0612,W0105,W0702,E0402


"timer"


import datetime
import re
import time as ttime


from ..client  import laps
from ..command import Command
from ..event   import Event
from ..find    import find
from ..runtime import broker
from ..timer   import Timer
from ..thread  import launch
from ..persist import whitelist
from ..object  import update
from ..workdir import sync


def init():
    for fnm, obj in find("timer"):
        if "time" not in obj:
            continue
        diff = float(obj.time) - ttime.time()
        if diff > 0:
            bot = broker.first()
            evt = Event()
            update(evt, obj)
            evt.orig = object.__repr__(bot)
            timer = Timer(diff, evt.show)
            launch(timer.start)


MONTHS = [
    'Bo',
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
]


FORMATS = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
]


class NoDate(Exception):

    pass


whitelist(Timer)


def extract_date(daystr):
    for fmt in FORMATS:
        try:
            res = ttime.mktime(ttime.strptime(daystr, fmt))
        except ValueError:
            res = None
        if res:
            return res


def get_day(daystr):
    day = None
    month = None
    yea = None
    try:
        ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
        if ymdre:
            (day, month, yea) = ymdre.groups()
    except ValueError:
        try:
            ymre = re.search(r'(\d+)-(\d+)', daystr)
            if ymre:
                (day, month) = ymre.groups()
                yea = ttime.strftime("%Y", ttime.localtime())
        except Exception as ex:
            raise NoDate(daystr) from ex
    if day:
        day = int(day)
        month = int(month)
        yea = int(yea)
        date = "%s %s %s" % (day, MONTHS[month], yea)
        return ttime.mktime(ttime.strptime(date, r"%d %b %Y"))
    raise NoDate(daystr)


def get_hour(daystr):
    try:
        hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmsre.group(1)))
        hoursmin = hours  + int(hmsre.group(2)) * 60
        hmsres = hoursmin + int(hmsre.group(3))
    except AttributeError:
        pass
    except ValueError:
        pass
    try:
        hmre = re.search(r'(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmre.group(1)))
        hmsres = hours + int(hmre.group(2)) * 60
    except AttributeError:
        return 0
    except ValueError:
        return 0
    return hmsres


def get_time(txt):
    try:
        target = get_day(txt)
    except NoDate:
        target = to_day(today())
    hour =  get_hour(txt)
    if hour:
        target += hour
    return target


def parse_time(txt):
    seconds = 0
    target = 0
    txt = str(txt)
    for word in txt.split():
        if word.startswith("+"):
            seconds = int(word[1:])
            return ttime.time() + seconds
        if word.startswith("-"):
            seconds = int(word[1:])
            return ttime.time() - seconds
    if not target:
        try:
            target = get_day(txt)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(txt)
        if hour:
            target += hour
    return target


def to_day(daystr):
    previous = ""
    line = ""
    daystr = str(daystr)
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = extract_date(line.strip())
        except ValueError:
            res = None
        if res:
            return res
        line = ""


def today():
    return str(datetime.datetime.today()).split()[0]


"commands"


def tmr(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('timer'):
            if "time" not in obj:
                continue
            lap = float(obj.time) - ttime.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {laps(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers")
        return
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply("%s is not an integer" % seconds)
                return
        else:
            line += word + " "
    if seconds:
        target = ttime.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or ttime.time() > target:
        event.reply("already passed given time.")
        return
    event.time = target
    diff = target - ttime.time()
    event.reply("ok " +  laps(diff))
    event.result = []
    event.result.append(event.rest)
    timer = Timer(diff, event.show, thrname=event.cmd)
    update(timer, event)
    sync(timer)
    launch(timer.start)


Command.add(tmr)
