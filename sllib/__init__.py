from contextlib import contextmanager

from .reader import Reader  # noqa: F401
from .frame import Frame

__all__ = ['Frame', 'Reader', 'create_reader']


@contextmanager
def create_reader(filename):
    reader = Reader(filename)
    try:
        yield reader
    finally:
        reader.close()
