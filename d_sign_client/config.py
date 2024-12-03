import sys
import configparser

from os.path import isfile, expanduser, join as pathjoin


CONFIG_NAME = 'placard.ini'
CONFIG_DIRS = [
    './', '~/.placard/', '/etc/placard/',
]
CONFIG_SECTION = 'placard'


def _config_paths():
    for dir in CONFIG_DIRS:
        path = expanduser(pathjoin(dir, CONFIG_NAME))
        if not isfile(path):
            continue
        yield path


def _read_config(paths):
    parser = configparser.ConfigParser()
    parser.read(paths)
    return parser


def _load_config():
    config = _read_config(_config_paths())
    for opt, value in config.items(CONFIG_SECTION):
        opt_upper = opt.upper()
        setattr(sys.modules[__name__], opt_upper, value)


_load_config()
