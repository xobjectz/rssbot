# This file is placed in the Public Domain.


"locks"


import _thread


brokerlock = _thread.allocate_lock()
disklock   = _thread.allocate_lock()
lock       = _thread.allocate_lock()
jsonlock   = _thread.allocate_lock()


def __dir__():
    return (
        'brokerlock',
        'disklock',
        'lock',
        'jsonlock'
    )
