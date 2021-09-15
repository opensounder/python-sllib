from sllib.errors import FieldNotFoundError
from typing import List, Tuple

import io
import logging
from .header import Header
from .frame import Frame
from .definitions import CALCULATED_FIELDS, FRAME_FIELDS

logger = logging.getLogger(__name__)


class Reader:
    header: Header
    _filter: dict

    def __init__(self, stream: io.IOBase, strict=False, **kwargs):
        if not isinstance(stream, io.IOBase):
            raise TypeError("stream is not an instance of io.IOBase")
        self.fs = stream
        self.header = Header.read(self.fs)
        self.format_version = [self.header.format, self.header.version]
        self.strict = strict
        self._filter = {'channels': [], 'fields': {}}

    @property
    def fields(self) -> List[str]:
        """generate a list of fieldnames for current format"""
        return FRAME_FIELDS[self.header.format] + CALCULATED_FIELDS

    @property
    def formver(self) -> Tuple[int]:
        """return format and version as a tuple"""
        return (self.header.format, self.header.version)

    def close(self):
        self.fs.close()

    def read(self, size):
        self.fs.read(size)

    def tell(self) -> int:
        return self.fs.tell()

    def add_filter(self, **kwargs):
        if 'channels' in kwargs:
            channels = kwargs.pop('channels')
            if not isinstance(channels, (list, tuple)):
                raise Exception('channels must be a list or tuple')
            self._filter['channels'] += channels

        fields = self.fields
        for key, value in kwargs.items():
            if key in fields:
                self._filter['fields'][key] = value
            else:
                raise FieldNotFoundError(f'{key} is not a valid field to filter on')
        return self

    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        r"""Reads next frame.

        :returns:
            A read frame instance
        """
        while True:
            frame = Frame.read(self.fs, self.format_version, self.header.framesize, strict=self.strict)
            if frame is None:
                raise StopIteration()
            if 'channels' in self._filter and self._filter['channels']:
                if frame.channel not in self._filter['channels']:
                    continue
            if not fieldsAllMatch(self._filter['fields'], frame):
                continue
            break
        return frame


def fieldsAllMatch(fields, frame) -> bool:
    result = True
    for key, value in fields.items():
        x = getattr(frame, key)
        if x != value:
            result = False
            break
    return result
