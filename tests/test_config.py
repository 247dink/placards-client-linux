import importlib

from unittest import TestCase

from d_sign_client.errors import ConfigError


CONFIG_MODULE = 'd_sign_client.config'


class ConfigTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.mod = importlib.import_module(CONFIG_MODULE)

    def test_config(self):
        self.assertEqual(self.mod.SERVER_URL, 'http://10.0.2.2:8000/')

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
