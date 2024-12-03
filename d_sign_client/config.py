import sys
import configparser

from os.path import isfile, expanduser, join as pathjoin
from types import ModuleType

from d_sign_client.errors import ConfigError


_NAME = 'placard.ini'
_DIRS = [
    './', '~/.placard/', '/etc/placard/',
]
_SECTION = 'placard'


def _read_config(paths=None):
    if paths is None:
        paths = [
            expanduser(pathjoin(dir, _NAME)) for dir in _DIRS
        ]
    parser = configparser.ConfigParser()
    parser.read(paths)
    return parser


class _ConfigModule(ModuleType):
    _config = None

    def __getattribute__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)

        try:
            return object.__getattribute__(self, name)

        except AttributeError:
            pass

        config = object.__getattribute__(self, '_config')
        if config is None:
            config = _read_config()
            setattr(self, '_config', config)

        try:
            value = config.get(_SECTION, name)

        except configparser.NoOptionError:
            raise ConfigError(name)

        setattr(self, name, value)
        return value


sys.modules[__name__].__class__ = _ConfigModule
