
from .header import Header
from .frame import Frame


class Reader:
    header: Header

    def __init__(self, filename, **kwargs):
        self.fs = open(filename, 'rb')
        self.header = Header.read(self.fs)

    def close(self):
        print('Closing')
        self.fs.close()

    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        r"""Reads next frame.

        :returns:
            A read frame instance
        """
        frame = Frame.read(self.fs, self.header.format)
        if frame is None:
            raise StopIteration()
        return frame
