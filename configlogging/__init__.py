"""Dead simple helper for configuring Python's logging module

For more details on logging config:

https://docs.python.org/library/logging.config.html
"""

import os
import json
import yaml
import logging.config

from ._compat import string_types


class ConfigException(Exception):
    """Base exception for configlogging module."""
    pass


def from_json(filename):
    """Configure logging module using JSON file."""
    with open(filename, 'r') as fileobj:
        config = json.load(fileobj)

    logging.config.dictConfig(config)


def from_yaml(filename):
    """Configure logging module using YAML file."""
    with open(filename, 'r') as fileobj:
        config = yaml.load(fileobj)

    logging.config.dictConfig(config)


def from_file(filename, **kargs):
    """Configure logging module using configparser-format file."""
    logging.config.fileConfig(filename, **kargs)


def from_dict(dct):
    """Configure logging module using dict object."""
    logging.config.dictConfig(dct)


def from_filename(filename):
    """Dispatch logging configuration based on filename extension."""
    ext = os.path.splitext(filename)[1]

    if ext in ('.json',):
        from_json(filename)
    elif ext in ('.yml', '.yaml'):
        from_yaml(filename)
    elif ext in ('.cfg', '.ini', '.conf', '.config'):
        from_file(filename)
    else:
        raise ConfigException(('Unrecognized filename extension. '
                               'Supported extensions: '
                               'json, yml, yaml, cfg, ini, conf, config'))


def from_autodetect(obj):
    """Dispatch logging configuration based on object type."""
    if isinstance(obj, dict):
        from_dict(obj)
    elif isinstance(obj, string_types):
        from_filename(obj)
    else:
        raise ConfigException(('Unable to autodetect object: {0}'
                               .format(repr(obj))))
