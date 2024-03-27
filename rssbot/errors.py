# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


""""deferred exception handling

This module allows for exceptions to be dealt with on a later moment.

"""


import io
import traceback


class Errors:

    errors = []
    filter = []
    output = None
    shown  = []

    @staticmethod
    def add(exc):
        "add an exception"
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def enable(out):
        "enable output"
        Errors.output = out

    @staticmethod
    def format(exc):
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

    @staticmethod
    def out(exc):
        "check if output function is set."
        if Errors.output:
            txt = str(Errors.format(exc))
            Errors.output(txt)

    @staticmethod
    def show():
        "show exceptions"
        for exc in Errors.errors:
            Errors.out(exc)

    @staticmethod
    def skip(txt):
        "check for skipping exceptions"
        for skp in Errors.filter:
            if skp in str(txt):
                return True
        return False


def debug(txt):
    "debug text"
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)


"interfacce"


def __dir__():
    return (
        'Errors',
        'debug'
    )


__all__ = __dir__()
