import struct
import logging

logger = logging.getLogger(__name__)


class Header(object):
    format: int = 0
    version: int = 0
    framesize: int = 0
    terminal: int = 0  # only used by format 1

    def __init__(self, format, version, framesize, debug, *args, **kwargs):
        self.format = format
        self.version = version
        self.framesize = framesize
        self.debug = debug

    def __str__(self):
        return (f'<Header(format={self.format}, version={self.version}, ' +
                f'framesize={self.framesize}, debug={self.debug})>')

    @staticmethod
    def read(filestream):
        data = struct.unpack("<HHHH", filestream.read(8))
        h = Header(*data)
        if h.format == 1:
            h.terminal = struct.unpack('<h', filestream.read(2))
        if logger.level == logging.DEBUG:
            logger.debug(h)
        return h
