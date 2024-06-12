# This file is placed in the Public Domain.


"deferred exception handling."


import io
import traceback


class Errors: # pylint: disable=R0903

    "Errors"

    errors = []
    out    = None

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
            Errors.out(Errors.format(exc)) # pylint: disable=E1102


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
