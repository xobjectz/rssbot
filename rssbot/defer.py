# This file is placed in the Public Domain.
# pylint: disable=W0125,E1102


"deferred exception handling."


import io
import traceback


class Errors:

    "Errors"

    errors = []
    out    = print

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
    def output(exc):
        "check if output function is set."
        if Errors.out:
            Errors.out(Errors.format(exc))


def errors():
    "show exceptions"
    for exc in Errors.errors:
        Errors.output(exc)


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


def __dir__():
    return (
        'Errors',
        'errors',
        'later'
    )
