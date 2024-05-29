# This file is placed in the Public Domain.


"mixin"


import unittest


from rssbot.object import Object


class Mix: # pylint: disable=R0903
    "class to mixin."

    a = "b"


class Mixin(Mix, Object): # pylint: disable=R0903

    "mixin class"


class TestMixin(unittest.TestCase):

    "test mixin classes."

    def test_mixin(self):
        "mixin test."
        mix = Mixin()
        self.assertTrue(isinstance(mix, Mixin))
