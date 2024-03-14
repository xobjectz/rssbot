# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"locks"


import _thread


"defines"


disklock   = _thread.allocate_lock()


"interface"


def __dir__():
    return (
        'disklock',
    )


__all__ = __dir__()
