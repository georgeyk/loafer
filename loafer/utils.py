from functools import wraps
import importlib
import os
import sys


def add_current_dir_to_syspath(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        current = os.getcwd()
        changed = False
        if current not in sys.path:
            sys.path.append(current)
            changed = True

        try:
            return f(*args, **kwargs)
        finally:
            # restore sys.path
            if changed is True:
                sys.path.remove(current)

    return wrapper


@add_current_dir_to_syspath
def import_callable(full_name):
    package, *name = full_name.rsplit('.', 1)
    try:
        module = importlib.import_module(package)
    except ValueError as exc:
        raise ImportError('Error trying to import {!r}'.format(full_name)) from exc

    if name:
        handler = getattr(module, name[0])
    else:
        handler = module

    if not callable(handler):
        raise ImportError('{!r} should be callable'.format(full_name))

    return handler
