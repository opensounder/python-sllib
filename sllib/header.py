import struct


class Header(object):
    format: int = 0
    version: int = 0
    framesize: int = 0

    def __init__(self, format, version, framesize, *args, **kwargs):
        self.format = format
        self.version = version
        self.framesize = framesize

    def __str__(self):
        return f'SlHeader(format={self.format}, version={self.version}, framesize={self.framesize})>'

    @staticmethod
    def read(filestream):
        data = struct.unpack("<HHHH", filestream.read(8))
        h = Header(*data)
        return h
