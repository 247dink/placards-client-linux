import importlib

from unittest import TestCase

from d_sign_client.errors import ConfigError


CONFIG_MODULE = 'd_sign_client.config'


class ConfigTestCase(TestCase):
    def test_config(self):
        mod = importlib.import_module(CONFIG_MODULE)
        self.assertEqual(mod.SERVER_URL, 'http://10.0.2.2:8000/')

    def test_missing(self):
        mod = importlib.import_module(CONFIG_MODULE)
        with self.assertRaises(ConfigError):
            mod.FOOBAR

    def test_protected(self):
        mod = importlib.import_module(CONFIG_MODULE)
        with self.assertRaises(AttributeError):
            mod._CONFIG
