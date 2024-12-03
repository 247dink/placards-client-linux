import importlib

from unittest import TestCase


class ConfigTestCase(TestCase):
    def test_config(self):
        mod = importlib.import_module('d_sign_client.config')
        self.assertEqual(mod.SERVER_URL, 'http://10.0.2.2:8000/')
