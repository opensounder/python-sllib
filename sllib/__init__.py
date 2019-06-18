
from .slreader import SlReader  # noqa: F401


class create_reader:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.reader = SlReader(filename=self.filename)
        return self.reader

    def __exit__(self, type, value, traceback):
        self.reader.close()
