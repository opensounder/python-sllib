from contextlib import contextmanager

from .reader import Reader  # noqa: F401
from .frame import Frame
from .header import Header

__all__ = ['Frame', 'Reader', 'Header', 'create_reader']


@contextmanager
def create_reader(filename):
    f = open(filename, 'rb')
    try:
        yield Reader(f)
    finally:
        f.close()


