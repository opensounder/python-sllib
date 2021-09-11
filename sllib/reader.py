import io
import logging
from .header import Header
from .frame import Frame

logger = logging.getLogger(__name__)


class Reader:
    header: Header

    def __init__(self, stream: io.IOBase, **kwargs):
        if not isinstance(stream, io.IOBase):
            raise TypeError("stream is not an instance of io.IOBase")
        self.fs = stream
        self.header = Header.read(self.fs)

    def close(self):
        self.fs.close()

    def read(self, size):
        self.fs.read(size)

    def tell(self) -> int:
        return self.fs.tell()

    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        r"""Reads next frame.

        :returns:
            A read frame instance
        """
        frame = Frame.read(self.fs, self.header.format, self.header.framesize)
        if frame is None:
            raise StopIteration()
        return frame
