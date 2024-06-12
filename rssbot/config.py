# This file is placed in the Public Domain.


"configuration"


from .default import Default


class Config(Default): # pylint: disable=R0903

    "Config"


def __dir__():
    return (
        'Config',
    )
