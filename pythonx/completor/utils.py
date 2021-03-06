# -*- coding: utf-8 -*-

import logging
import functools

from ._vim import vim_obj


logger = logging.getLogger('completor')


def ignore_exception(fallback=()):
    """Ignore exception raised by the decorated function.

    When exception happened the fallback value is returned.
    """
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                return fallback
        return wrapper
    return deco


class _highlight(object):
    HIGHLIGHT_GROUP_MAP = {
        'warn': 'WarningMsg',
        'error': 'ErrorMsg'
    }

    def __init__(self, severity):
        self.severity = severity

    def _echohl(self, group):
        vim_obj.command('echohl {}'.format(group))

    def __enter__(self):
        self._echohl(self.HIGHLIGHT_GROUP_MAP.get(self.severity, 'Normal'))

    def __exit__(self, et, ev, tb):
        self._echohl('None')


def echo(message, severity='info'):
    """Print message to vim message area.

    :param message: The message to print.
    :param severity: Available values: info(the default), warn, error.
    """
    with _highlight(severity):
        vim_obj.command('echo {!r}'.format(message))
