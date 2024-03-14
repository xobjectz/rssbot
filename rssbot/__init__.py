# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0613,E0101,E0402


"interface"


from .decoder import loads
from .encoder import dumps
from .objects import *


def __dir__():
    return (
        'Object',
        'construct',
        'dumps',
        'edit',
        'fmt',
        'fqn',
        'ident',
        'items',
        'keys',
        'loads',
        'search',
        'update',
        'values',
    )
