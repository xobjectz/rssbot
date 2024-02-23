# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212


"utilities"


import os
import pathlib
import pwd
import sys
import termios
import time
import types
import _thread


def __dir__():
    return (
        'cdir',
        'checkpid',
        'daemon',
        'fntime',
        'forever',
        'getpid',
        'name',
        'privileges',
        'strip',
        'wrap'
    )


__all__ = __dir__()


def cdir(pth) -> None:
    if os.path.exists(pth):
        return
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def checkpid(pid):
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def fntime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def getpid(path):
    try:
        return int(open(path, encoding="utf-8").read())
    except (FileNotFoundError, ValueError):
        return None


def name(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


def wrap(func):
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)
