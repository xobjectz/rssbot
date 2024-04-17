# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"errors"


import io
import traceback


class Errors:

    "Errors"

    errors = []


    @staticmethod
    def out(txt):
        "overload this."


def debug(txt):
    Errors.out(txt)


def enable(func):
    Errors.out = func


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


def tostr(exc):
    "format an exception"
    res = ""
    stream = io.StringIO(
                         traceback.print_exception(
                                                   type(exc),
                                                   exc,
                                                   exc.__traceback__
                                                  )
                        )
    for line in stream.readlines():
        res += line + "\n"
    return res


def out(exc):
    "check if output function is set."
    txt = str(tostr(exc))
    Errors.out(txt)


def errors():
    "show exceptions"
    for exc in Errors.errors:
        out(exc)
