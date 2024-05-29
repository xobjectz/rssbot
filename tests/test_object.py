# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"objects"


import unittest


from rssbot.object import Object, fmt, fqn, items, keys, update, values


VALIDJSON = '{"test": "bla"}'


attrs1 = (
    "Object",
    "clear",
    "copy",
    "fromkeys",
    "get",
    "items",
    "keys",
    "matchkey",
    "pop",
    "popitem",
    "save",
    "setdefault",
    "update",
    "values",
)

attrs2 = (
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__fnm__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__slots__",
    "__str__",
    "__subclasshook__",
)


class TestObject(unittest.TestCase):


    "Object related tests."

    def test_constructor(self):
        "constructor test."
        obj = Object()
        self.assertTrue(type(obj), Object)

    def test_class(self):
        "test proper class."
        obj = Object()
        clz = obj.__class__()
        self.assertTrue("Object" in str(type(clz)))

    def test_contains(self):
        "test containment."
        obj = Object()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        "test deleting of attribute."
        obj = Object()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        "test __dict__"
        obj = Object()
        self.assertEqual(obj.__dict__, {})

    def test_format(self):
        "test __format__"
        obj = Object()
        self.assertEqual(obj.__format__(""), "{}")

    def test_getattribute(self):
        "test attributing."
        obj = Object()
        obj.key = "value"
        self.assertEqual(obj.__getattribute__("key"), "value")

    def test_hash(self):
        "test for hash being an integer."
        obj = Object()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        "test constructor."
        obj = Object()
        self.assertTrue(type(Object.__init__(obj)), Object)

    def test_iter(self):
        "test iteration."
        obj = Object()
        obj.key = "value"
        self.assertTrue(
            list(obj.__iter__()),
            [
                "key",
            ],
        )

    def test_len(self):
        "test length calcualtion."
        obj = Object()
        self.assertEqual(len(obj), 0)

    def test_module(self):
        "test module name."
        self.assertEqual(Object().__module__, "rssbot.object")

    def test_fqn(self):
        "test full qualified domain name."
        self.assertEqual(fqn(Object()), "rssbot.object.Object")

    def test_repr(self):
        "test representation."
        self.assertTrue(update(Object(), {"key": "value"}).__repr__(), {"key": "value"})

    def test_setattr(self):
        "test setting of attribute."
        obj = Object()
        obj.__setattr__("key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        "test stringify."
        obj = Object()
        self.assertEqual(str(obj), "{}")

    def test_fmt(self):
        "test object format."
        obj = Object()
        self.assertEqual(fmt(obj), "")

    def test_getattr(self):
        "test retrieving of attributes."
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_keys(self):
        "test returning of keys."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(keys(obj)),
            [
                "key",
            ],
        )

    def test_items(self):
        "test items of object."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(items(obj)),
            [
                ("key", "value"),
            ],
        )

    def test_register(self):
        "test setting attribute."        
        obj = Object()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_update(self):
        "test updating of object."
        obj = Object()
        obj.key = "value"
        oobj = Object()
        update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        "test values of an object."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(values(obj)),
            [
                "value",
            ],
        )
