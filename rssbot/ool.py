# This file is placed in the Public Domain.


"object of lists"


from .object import Object


class OoL(Object):


    def add(self, name, val):
        if name not in self:
            setattr(self, name, [])
        lll = getattr(self, name)
        lll.append(val)


    def extend(self, name, lis=[]):
        if name not in self:
            setattr(self, name, lis)
        lll = getattr(self, name)
        lll.extend(lis)
