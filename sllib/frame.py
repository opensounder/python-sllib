import struct
import math
import io
from typing import Tuple
import logging

from sllib.definitions import (
    CALCULATED_FIELDS, EARTH_RADIUS, FEET_CONVERSION, FLAG_FORMATS,
    FRAME_DEFINITIONS, FRAME_FIELDS, FRAME_FORMATS,
    KNOTS_KMH, RAD_CONVERSION
)
# from .debug import print_attributes

__all__ = ['Frame']

logger = logging.getLogger(__name__)


class Frame(object):
    gps_speed: int = 0
    lat_enc: int = 0
    lon_enc: int = 0
    water_depth: int = 0
    time1: int = 0

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def heading_deg(self):
        return self.heading * RAD_CONVERSION

    @property
    def gps_speed_kph(self):
        return self.gps_speed * KNOTS_KMH

    @property
    def longitude(self):
        return self.lon_enc / EARTH_RADIUS * RAD_CONVERSION

    @property
    def latitude(self):
        temp = math.exp(self.lat_enc / EARTH_RADIUS)
        temp = (2 * math.atan(temp)) - (math.pi / 2)
        return temp * RAD_CONVERSION

    @property
    def water_depth_m(self):
        return self.water_depth * FEET_CONVERSION

    def to_dict(self, format=2, fields=None):
        out = {}
        allfields = FRAME_FIELDS[format] + CALCULATED_FIELDS
        if fields is not None:
            allfields = list(filter(lambda x: x in allfields, fields))
        for name in allfields:
            if hasattr(self, name):
                out[name] = getattr(self, name)
            else:
                out[name] = 0

        return out

    @staticmethod
    def read(stream: io.IOBase, format: int, blocksize: int = 0):
        if format == 1:
            # slg is a conditional format for each packet... yuck
            return _readSlg(stream, blocksize)
        if format == 2:
            return _readSlx(stream, blocksize, 2)
        if format == 3:
            return _readSlx(stream, blocksize, 3)

        f = FRAME_FORMATS[format]
        s = struct.calcsize(f)
        here = stream.tell()
        while True:
            buf = stream.read(s)
            if buf == b'':
                # EOF
                return None
            if len(buf) < s:
                print(f'This is bad. Only got {len(buf)}/{s} bytes=', buf)
                raise Exception("this is bad")
            data = struct.unpack(f, buf)
            if data[0] == here:  # offset is allways first
                break
            elif here > 0:
                # jump forward and try to catch next
                here += 1
                stream.seek(here)
                continue
            else:
                raise Exception('location does not match expected offset')

        kv = {'headersize': s}
        for i, d in enumerate(FRAME_DEFINITIONS[format]):
            name = d['name']
            if not name == "-":
                kv[name] = data[i]

        b = Frame(**kv)
        # print('packet at', filestream.tell(), b.to_dict(format=format, fields=['offset', 'packetsize', 'longitude']))
        b.packet = stream.read(b.packetsize)
        # print('post packet offset:', filestream.tell())
        return b


def _readSlx(stream: io.IOBase, blocksize: int, format: int) -> Frame:
    f = FRAME_FORMATS[format]
    s = struct.calcsize(f)
    here = stream.tell()
    bad = 0
    while True:
        buf = stream.read(s)
        if buf == b'':
            # EOF
            return None
        if len(buf) < s:
            print(f'This is bad. Only got {len(buf)}/{s} bytes=', buf)
            raise Exception("this is bad")
        data = struct.unpack(f, buf)
        if data[0] == here:  # offset is allways first
            if bad > 1:
                logger.warn('got back at offset: %s', here)
            break
        elif here > 0:
            bad += 1
            if bad == 1:
                logger.warn('unexpected offset at offset: %s. will try to find next frame', here)
            # jump forward and try to catch next
            here += 1
            stream.seek(here)
            continue
        else:
            raise Exception('location does not match expected offset')

    kv = {'headersize': s}
    for i, d in enumerate(FRAME_DEFINITIONS[format]):
        name = d['name']
        if not name == "-":
            kv[name] = data[i]
            if name == 'flags' and FLAG_FORMATS[format]:
                flagform = FLAG_FORMATS[format]
                flags = data[i]
                for k, v in flagform.items():
                    kv[k] = flags & v == v
    b = Frame(**kv)
    if b.has_packet:
        b.packet = stream.read(b.packetsize)
    else:
        logger.debug(
            'frame with bad packet. offset: %s channel: %s, index: %s',
            b.offset, b.channel, b.frame_index
        )
        stream.read(b.framesize - s)
    # print('post packet offset:', filestream.tell())
    return b


def _readSlg(fs: io.IOBase, blocksize: int) -> Frame:
    start = fs.tell()
    # show(fs, '--- start')
    # fs.read(1)  # skip 1
    headerlen = 2
    try:
        flags = unreadpack(fs, '<H')[0]
    except EOFError:
        return None
    kv = {'flags': flags}
    f = _FlagsF1(flags)
    # print(f'-- {start}\t| {hex(start)}\t> {flags:016b}')
    # print_attributes(f)

    if flags > 0:
        try:
            # B=byte, H=ushort, h=short, I=uint, i=int, f=float
            if f.has_depth | f.has_surface_depth:
                kv['lower_limit'] = unreadpack(fs, '<f')[0]
            if f.has_depth | f.has_surface_depth:
                kv['water_depth'] = unreadpack(fs, '<f')[0]
            if f.has_temp:
                kv['water_temperature'] = unreadpack(fs, '<f')[0]
            if f.has_waterspeed:
                kv['water_speed'] = unreadpack(fs, '<f')[0]
            if f.has_position:
                data = unreadpack(fs, '<II')
                kv['lon_enc'] = data[0]
                kv['lat_enc'] = data[1]
            if f.has_surface_depth:
                kv['surface_depth'] = unreadpack(fs, '<f')[0]
            if f.has_tob:
                kv['top_of_bottom'] = unreadpack(fs, '<f')[0]
            if f.has_temp2:
                kv['temp2'] = unreadpack(fs, '<f')[0]
            if f.has_temp3:
                kv['temp3'] = unreadpack(fs, '<f')[0]
            if f.has_time:
                kv['time1'] = unreadpack(fs, '<I')[0]
            if f.has_speed_track:
                data = unreadpack(fs, '<ff')
                kv['gps_speed'] = data[0]
                kv['heading'] = data[1]
            if f.test_valid_alititude:
                kv['altitude'] = unreadpack(fs, '<f')[0]
            else:
                data = unreadpack(fs, '<ff')
                kv['other'] = data[0]
                kv['altitude'] = data[1]
            # show(fs, 'before packet')
            kv['packetsize'] = unreadpack(fs, '<H')[0]
        except EOFError:
            return None
    # else:
        # data = []
        # print('Unknown flags', flags)

    # show(fs, 'end')
    headerlen = fs.tell() - start
    kv['headerlen'] = headerlen
    calc_size = blocksize-headerlen
    packet_size = kv['packetsize']
    # print(f'headerlen={headerlen}, calc size={calc_size}, pz={packet_size}')
    b = Frame(**kv)
    # print_attributes(b)
    if calc_size != packet_size:
        raise Exception(f'missmatched packetsize. got {packet_size} want {calc_size}')
    b.packet = fs.read(blocksize-headerlen)
    return b


# def show(fs: io.IOBase, msg: str = ''):
#     p = fs.tell()
#     print(str.strip('%s here %d, %s' % (msg, p, hex(p))))


def unreadpack(fs: io.IOBase, f: str) -> Tuple:
    s = struct.calcsize(f)
    buf = fs.read(s)
    if buf == b'':
        raise EOFError
    if len(buf) != s:
        raise Exception('not enough data')
    return struct.unpack(f, buf)


class _FlagsF1(object):
    value: int = 0

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def _is_set(self, mask: int) -> bool:
        return self.value & mask == mask

    @property
    def test_valid_alititude(self) -> bool:
        return not ((self.has_time or self.has_speed_track) and self.has_altitude)

    @property
    def has_altitude(self) -> bool:
        return self._is_set(0x0001)

    @property
    def has_temp(self) -> bool:
        return self._is_set(0x0010)

    @property
    def has_temp2(self) -> bool:
        return self._is_set(0x0020)

    @property
    def has_temp3(self) -> bool:
        return self._is_set(0x0040)

    @property
    def has_waterspeed(self) -> bool:
        return self._is_set(0x0080)

    @property
    def has_position(self):
        return self._is_set(0x0100)

    @property
    def has_depth(self) -> bool:
        return self._is_set(0x0200)

    @property
    def has_surface_depth(self) -> bool:
        return self._is_set(0x0400)

    @property
    def has_tob(self) -> bool:
        return self._is_set(0x0800)

    @property
    def has_time(self) -> bool:
        return self._is_set(0x2000)

    @property
    def has_speed_track(self) -> bool:
        return self._is_set(0x4000)
