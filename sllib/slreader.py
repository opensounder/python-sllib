
from .slheader import SlHeader
from .slblock import SlBlock


class SlReaderMeta:
    pass


class SlReader:
    header: SlHeader

    def __init__(self, filename, **kwargs):
        self.header = SlHeader()

    def close(self):
        print('Closing')

    def __iter__(self):
        return self

    def __next__(self) -> SlBlock:
        r"""Reads next block.

        :returns:
            A read block instance or None
        """
        raise StopIteration()
