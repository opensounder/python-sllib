from contextlib import contextmanager

from .reader import Reader  # noqa: F401
from .frame import Frame

__all__ = ['Frame', 'Reader', 'create_reader']


@contextmanager
def create_reader(filename):
    f = open(filename, 'rb')
    try:
        yield Reader(f)
    finally:
        f.close()
