import struct


class SlHeader(object):
    format: int = 0
    version: int = 0
    blocksize: int = 0

    def __init__(self, format, version, blocksize, *args, **kwargs):
        self.format = format
        self.version = version
        self.blocksize = blocksize

    def __str__(self):
        return f'SlHeader(format={self.format}, version={self.version}, blocksize={self.blocksize})>'

    @staticmethod
    def read(filestream):
        data = struct.unpack("<HHHH", filestream.read(8))
        h = SlHeader(*data)
        return h
