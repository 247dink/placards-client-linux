import importlib

from unittest import TestCase

from placards.errors import ConfigError


CONFIG_MODULE = 'placards.config'


class ConfigTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.mod = importlib.import_module(CONFIG_MODULE)

    def test_config(self):
        self.assertEqual(self.mod.SERVER_URL, 'https://fishers.facman.site/')

    def test_missing(self):
        with self.assertRaises(ConfigError):
            self.mod.FOOBAR

    def test_protected(self):
        with self.assertRaises(AttributeError):
            self.mod._CONFIG

    def test_get(self):
        self.assertIsNone(self.mod.get('MISSING', None))
        with self.assertRaises(ConfigError):
            self.mod.get('MISSING')

    def test_int(self):
        self.assertEqual(1, self.mod.getint('test_int'))
        self.assertEqual(1, self.mod.getint('test_float'))

    def test_float(self):
        self.assertEqual(1.0, self.mod.getfloat('test_float'))

    def test_bool(self):
        self.assertTrue(self.mod.getbool('test_int'))
        self.assertTrue(self.mod.getbool('test_bool_on'))
        self.assertFalse(self.mod.getbool('test_bool'))
