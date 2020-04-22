from contextlib import contextmanager

from .reader import Reader  # noqa: F401


@contextmanager
def create_reader(filename):
    reader = Reader(filename)
    try:
        yield reader
    finally:
        reader.close()
