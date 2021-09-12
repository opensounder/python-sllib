from contextlib import contextmanager

from .reader import Reader  # noqa: F401
from .frame import Frame
from .header import Header

__all__ = ['Frame', 'Reader', 'Header', 'create_reader', '__version__']

__version__ = '0.2.3'

@contextmanager
def create_reader(filename, strict=False):
    f = open(filename, 'rb')
    try:
        yield Reader(f, strict=strict)
    finally:
        f.close()
