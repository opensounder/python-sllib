
from .slheader import SlHeader
from .slblock import SlBlock, build_pattern


class SlReaderMeta:
    pass


class SlReader:
    header: SlHeader

    def __init__(self, filename, **kwargs):
        self.fs = open(filename, 'rb')
        self.header = SlHeader.read(self.fs)

    def close(self):
        print('Closing')
        self.fs.close()

    def __iter__(self):
        return self

    def __next__(self) -> SlBlock:
        r"""Reads next block.

        :returns:
            A read block instance
        """
        block = SlBlock.read(self.fs, self.header.format)
        if block is None:
            raise StopIteration()
        return block
