# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys
import time
import functools

# This makes mocking easier
output = sys.stdout
error = sys.stderr


def print_result(*args):
    print(*args, file=output)  # noqa


def print_info(message):
    print('[INFO] {message}'.format(message=message), file=error)  # noqa


def print_error(message):
    RED = '\033[31m'
    END = '\033[0m'
    print('{color}[ERROR]{end} {message}'.format(color=RED, end=END, message=message), file=error)  # noqa


def print_warning(message):
    YELLOW = '\033[33m'
    END = '\033[0m'
    print('{color}[WARNING]{end} {message}'.format(color=YELLOW, end=END, message=message), file=error)  # noqa


def print_help(*args):
    GREEN = '\033[32m'
    END = '\033[0m'
    print('{color}{}{end} '.format(*args, color=GREEN, end=END), file=error)  # noqa

def try_and_print_error(f):
    functools.wraps(f)

    def _f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            print_error(e)

    return _f
