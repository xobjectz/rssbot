# This file is placed in the Public Domain.


"classes"


import inspect


from .disk    import Workdir
from .object  import Object


class Classes: # pylint: disable=R0903

    "Whitelist"

    classes = Object()

    @staticmethod
    def long(name):
        "match from single name to long name."
        split = name.split(".")[-1].lower()
        res = name
        for named in Classes.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        if "." not in res:
            for fnm in Workdir.types():
                claz = fnm.split(".")[-1]
                if fnm == claz.lower():
                    res = fnm
        return res

    @staticmethod
    def whitelist(clz):
        "add class to whitelist."
        name = str(clz).split()[1][1:-2]
        setattr(Classes.classes, name, clz)


def scancls(mod) -> None:
    "scan module for classes."
    for key, clz in inspect.getmembers(mod, inspect.isclass):
        if key.startswith("cb"):
            continue
        if not issubclass(clz, Object):
            continue
        Classes.whitelist(clz)


def __dir__():
    return (
        "Classes",
        "scancls"
    )
