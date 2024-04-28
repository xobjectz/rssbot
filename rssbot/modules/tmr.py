# This file is placed in the Public Domain.


"timer"


import datetime
import re
import time as ttime


from ..client    import laps
from ..event     import Event
from ..find      import find
from ..object    import update
from ..runtime   import broker
from ..thread    import launch
from ..timer     import Timer
from ..workdir   import sync


def init():
    "start timers."
    for _fn, obj in find("timer"):
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

    "NoDate"


def extract_date(daystr):
    "extract date from string."
    res = None
    for fmt in FORMATS:
        try:
            res = ttime.mktime(ttime.strptime(daystr, fmt))
            break
        except ValueError:
            res = None
    return res


def get_day(daystr):
    "return day from string."
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
        except Exception as ex: # pylint: disable=W0212
            raise NoDate(daystr) from ex
    if day:
        day = int(day)
        month = int(month)
        yea = int(yea)
        date = f"{day} {MONTHS[month]} {yea}"
        return ttime.mktime(ttime.strptime(date, r"%d %b %Y"))
    raise NoDate(daystr)


def get_hour(daystr):
    "return hour from string."
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
    "parse full time string."
    try:
        target = get_day(txt)
    except NoDate:
        target = to_day(today())
    hour =  get_hour(txt)
    if hour:
        target += hour
    return target


def parse_time(txt):
    "parse time from string."
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
    "parse day from string."
    previous = ""
    line = ""
    daystr = str(daystr)
    res = None
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = extract_date(line.strip())
            break
        except ValueError:
            res = None
        line = ""
    return res


def today():
    "return date."
    return str(datetime.datetime.today()).split()[0]


def tmr(event):
    "add a timer."
    result = ""
    if not event.rest:
        nmr = 0
        for _fn, obj in find('timer'):
            lap = float(obj.time) - ttime.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {laps(lap)}')
                nmr += 1
        return result
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply(f"{seconds} is not an integer")
                return result
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
        return result
    event.time = target
    diff = target - ttime.time()
    event.reply("ok " +  laps(diff))
    event.result = []
    event.result.append(event.rest)
    timer = Timer(diff, event.show, thrname=event.cmd)
    update(timer, event)
    sync(timer)
    launch(timer.start)
    return result
