# This file is placed in the Public Domain.
# pylint: disable=R0912


"timer"


import datetime
import re
import time as ttime


from rssbot.cmds   import add
from rssbot.disk   import find, sync
from rssbot.run    import fleet
from rssbot.timer  import Timer
from rssbot.utils  import laps
from rssbot.launch import launch


def init():
    "initialaze modules."
    for _fnm, obj in find("timer"):
        diff = float(obj.time) - ttime.time()
        if diff > 0:
            timer = Timer(diff, fleet.announce, obj.rest)
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

    "can't parse date."


def extract_date(daystr):
    "extract date from string."
    res = None
    for fmtt in FORMATS:
        try:
            res = ttime.mktime(ttime.strptime(daystr, fmtt))
            break
        except ValueError:
            pass
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
        except Exception as ex:
            raise NoDate(daystr) from ex
    if day:
        day = int(day)
        month = int(month)
        yea = int(yea)
        date = f"{day} {MONTHS[month]} {yea}"
        return ttime.mktime(ttime.strptime(date, r"%d %b %Y"))
    raise NoDate(daystr)


def get_hour(daystr):
    "get hour from string."
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
    "return time from string."
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
    "scan string for day/time."
    previous = ""
    line = ""
    daystr = str(daystr)
    res = None
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = extract_date(line.strip())
        except ValueError:
            res = None
        if res:
            break
        line = ""
    return res

def today():
    "return time of today."
    return str(datetime.datetime.today()).split()[0]


def tmr(event):
    "set timer."
    res = None
    if not event.rest:
        nmr = 0
        for _fnm, obj in find('timer'):
            lap = float(obj.time) - ttime.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.rest} {laps(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers")
        return res
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply(f"{seconds} is not an integer")
                return res
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
        return res
    diff = target - ttime.time()
    event.reply("ok " +  laps(diff))
    timer = Timer(diff, fleet.announce, event.rest, thrname=event.cmd)
    timer.time = target
    timer.rest = event.rest
    sync(timer)
    launch(timer.start)
    return res


add(tmr)
