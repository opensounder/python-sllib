import struct
import math

__all__ = ['Frame']

KNOTS_KMH = 1.85200
EARTH_RADIUS = 6356752.3142
RAD_CONVERSION = 180 / math.pi
FEET_CONVERSION = 0.3048

F0_FRAME = ()

F1_FRAME = (
    {'name': 'offset', 'type': 'I'},
    {'name': 'previous_primary_offset', 'type': 'I'},
    {'name': 'previous_secondary_offset', 'type': 'I'},
    {'name': 'previous_downscan_offset', 'type': 'I'},
    {'name': 'previous_left_sidescan_offset', 'type': 'I'},
    {'name': 'previous_right_sidescan_offset', 'type': 'I'},
    {'name': 'previous_composite_sidescan_offset', 'type': 'I'},
    {'name': 'framesize', 'type': 'H'},
    {'name': 'previous_framesize', 'type': 'H'},
    {'name': 'channel', 'type': 'H'},
    {'name': 'packetsize', 'type': 'H'},
    {'name': 'frame_index', 'type': 'I'},
    {'name': 'upper_limit', 'type': 'f'},
    {'name': 'lower_limit', 'type': 'f'},
    {'name': '-', 'type': '2s'},
    {'name': 'frequency', 'type': 'B'},
    {'name': '-', 'type': '13s'},
    {'name': 'water_depth', 'type': 'f'},
    {'name': 'keel_depth', 'type': 'f'},
    {'name': '-', 'type': '28s'},
    {'name': 'gps_speed', 'type': 'f'},
    {'name': 'temperature', 'type': 'f'},
    {'name': 'lon_enc', 'type': 'I'},
    {'name': 'lat_enc', 'type': 'I'},
    {'name': 'water_speed', 'type': 'f'},
    {'name': 'course', 'type': 'f'},
    {'name': 'altitude', 'type': 'f'},
    {'name': 'heading', 'type': 'f'},
    {'name': 'flags', 'type': 'H'},
    {'name': '-', 'type': '6s'},
    {'name': 'time1', 'type': 'I'},
)
F3_FRAME = (
    {'name': 'offset', 'type': 'I'},
    {'name': 'framesize', 'type': 'H'},
    {'name': 'previous_framesize', 'type': 'H'},
    {'name': 'channel', 'type': 'H'},
    {'name': 'frame_index', 'type': 'I'},
    {'name': 'upper_limit', 'type': 'f'},
    {'name': 'lower_limit', 'type': 'f'},
    {'name': '-', 'type': '12s'},
    {'name': 'created_at', 'type': 'I'},
    {'name': 'packetsize', 'type': 'H'},
    {'name': 'water_depth', 'type': 'f'},
    {'name': 'frequency', 'type': 'B'},
    {'name': 'gps_speed', 'type': 'f'},
    {'name': 'temperature', 'type': 'f'},
    {'name': 'lon_enc', 'type': 'I'},
    {'name': 'lat_enc', 'type': 'I'},
    {'name': 'water_speed', 'type': 'f'},
    {'name': 'course', 'type': 'f'},
    {'name': 'altitude', 'type': 'f'},
    {'name': 'heading', 'type': 'f'},
    {'name': 'flags', 'type': 'H'},
    {'name': 'time1', 'type': 'I'},
    {'name': 'previous_primary_offset', 'type': 'I'},
    {'name': 'previous_secondary_offset', 'type': 'I'},
    {'name': 'previous_downscan_offset', 'type': 'I'},
    {'name': 'previous_left_sidescan_offset', 'type': 'I'},
    {'name': 'previous_right_sidescan_offset', 'type': 'I'},
    {'name': 'previous_composite_sidescan_offset', 'type': 'I'},
    {'name': '-', 'type': '12s'},
    {'name': 'previous_dc_offset', 'type': 'I'},
)

FRAME_DEFINITIONS = (
    F0_FRAME,
    F1_FRAME,
    F1_FRAME,
    F3_FRAME,
)


def build_pattern(fdef):
    return "<" + "".join(map(lambda x: x['type'], fdef))


def build_names(fdef):
    return list(map(lambda x: x['name'],
                filter(lambda x: x['name'] != '-', fdef)))


FRAME_FORMATS = (
    build_pattern(FRAME_DEFINITIONS[0]),
    build_pattern(FRAME_DEFINITIONS[1]),
    build_pattern(FRAME_DEFINITIONS[2]),
    build_pattern(FRAME_DEFINITIONS[3]),
)

FRAME_FIELDS = (
    build_names(FRAME_DEFINITIONS[0]),
    build_names(FRAME_DEFINITIONS[1]),
    build_names(FRAME_DEFINITIONS[2]),
    build_names(FRAME_DEFINITIONS[3]),
)

CALCULATED_FIELDS = ['gps_speed_kph', 'longitude', 'latitude', 'water_depth_m']


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
    def read(filestream, format):
        f = FRAME_FORMATS[format]
        s = struct.calcsize(f)
        buf = filestream.read(s)
        if buf == b'':
            # EOF
            return None
        if len(buf) < s:
            print(f'This is bad. Only got {len(buf)}/{s} bytes=', buf)
            raise Exception("this is bad")

        data = struct.unpack(f, buf)
        kv = {}
        for i, d in enumerate(FRAME_DEFINITIONS[format]):
            if not d['name'] == "-":
                kv[d['name']] = data[i]
        b = Frame(**kv)
        b.packet = filestream.read(b.packetsize)
        return b
