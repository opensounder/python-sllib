import struct
F0_BLOCK = ()

F2_BLOCK = (
    {'name': 'offset', 'type': 'I'},
    {'name': 'previous_primary_offset', 'type': 'I'},
    {'name': 'previous_secondary_offset', 'type': 'I'},
    {'name': 'previous_downscan_offset', 'type': 'I'},
    {'name': 'previous_left_sidescan_offset', 'type': 'I'},
    {'name': 'previous_right_sidescan_offset', 'type': 'I'},
    {'name': 'previous_composite_sidescan_offset', 'type': 'I'},
    {'name': 'blocksize', 'type': 'H'},
    {'name': 'previous_blocksize', 'type': 'H'},
    {'name': 'channel', 'type': 'H'},
    {'name': 'packetsize', 'type': 'H'},
    {'name': 'block_index', 'type': 'I'},
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
F3_BLOCK = (
    {'name': 'offset', 'type': 'I'},
    {'name': 'blocksize', 'type': 'H'},
    {'name': 'previous_blocksize', 'type': 'H'},
    {'name': 'channel', 'type': 'H'},
    {'name': 'block_index', 'type': 'I'},
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

BLOCK_DEFINITIONS = (
    F0_BLOCK,
    F2_BLOCK,
    F2_BLOCK,
    F3_BLOCK,
)


def build_pattern(pat):
    return "<" + "".join(map(lambda x: x['type'], pat))


BLOCK_FORMATS = (
    build_pattern(BLOCK_DEFINITIONS[0]),
    build_pattern(BLOCK_DEFINITIONS[1]),
    build_pattern(BLOCK_DEFINITIONS[2]),
    build_pattern(BLOCK_DEFINITIONS[3]),
)


class SlBlock(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def read(filestream, format):
        f = BLOCK_FORMATS[format]
        s = struct.calcsize(f)
        buf = filestream.read(s)
        if buf == '':
            # EOF
            return None
        if len(buf) < s:
            print(f'This is bad. Only got {len(buf)}/{s} bytes=', buf)
            return None
        data = struct.unpack(f, buf)
        kv = {}
        for i, d in enumerate(BLOCK_DEFINITIONS[format]):
            if not d['name'] == "-":
                kv[d['name']] = data[i]
        b = SlBlock(**kv)
        b.packet = filestream.read(b.packetsize)
        return b
