from contextlib import contextmanager

from .slreader import SlReader  # noqa: F401


@contextmanager
def create_reader(filename):
    reader = SlReader(filename)
    try:
        yield reader
    finally:
        reader.close()
