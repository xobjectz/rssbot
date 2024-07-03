# This file is placed in the Public Domain.
# pylint: disable=R0902,R0903


"configuration"


from .dft import Default


class Config(Default):

    "Config"


def __dir__():
    return (
        'Config',
    )
