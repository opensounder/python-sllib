import math

KNOTS_KMH = 1.85200
EARTH_RADIUS = 6356752.3142
RAD_CONVERSION = 180 / math.pi
FEET_CONVERSION = 0.3048

F0_FRAME = ()
# B=byte, H=ushort, h=short, I=uint, i=int, f=float
F1_FRAME = (
    # {'name': 'flags', 'type': 'H'},
    # {'name': 'lower_limit', 'type': 'f'},
    # {'name': 'water_depth', 'type': 'f'},
    # {'name': 'temperature', 'type': 'f'},
    # {'name': 'water_speed', 'type': 'f'},
    # {'name': 'lon_enc', 'type': 'i'},
    # {'name': 'lat_enc', 'type': 'i'},
    # {'name': 'surface_depth', 'type': 'f'},
    # {'name': 'top_of_bottom', 'type': 'f'},
    # {'name': 'temperature2', 'type': 'f'},
    # {'name': 'temperature3', 'type': 'f'},
    # {'name': 'time1', 'type': 'I'},
    # {'name': 'gps_speed', 'type': 'f'},
    # {'name': 'heading', 'type': 'f'},
    # {'name': 'altitude', 'type': 'f'},
    # {'name': 'packetsize', 'type': 'H'},
)
F2_FRAME = (
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
    {'name': 'lon_enc', 'type': 'i'},
    {'name': 'lat_enc', 'type': 'i'},
    {'name': 'water_speed', 'type': 'f'},
    {'name': 'course', 'type': 'f'},
    {'name': 'altitude', 'type': 'f'},
    {'name': 'heading', 'type': 'f'},
    {'name': 'flags', 'type': 'H'},
    {'name': '-', 'type': '6s'},
    {'name': 'time1', 'type': 'I'},
)
# H = ushort(2), I= uint(4)
F3_FRAME = (
    {'name': 'offset', 'type': 'I'},
    # {'name': 'a', 'type': 'H'},
    # {'name': 'b', 'type': 'H'},
    {'name': '-', 'type': 'I'},
    {'name': 'framesize', 'type': 'H'},
    {'name': 'previous_framesize', 'type': 'H'},
    # {'name': 'framesize', 'type': 'I'},
    # {'name': 'previous_framesize', 'type': 'I'},
    {'name': 'channel', 'type': 'I'},
    {'name': 'frame_index', 'type': 'I'},
    {'name': 'lower_limit', 'type': 'f'},
    {'name': 'upper_limit', 'type': 'f'},
    {'name': '-', 'type': '12s'},
    {'name': 'created_at', 'type': 'I'},
    {'name': 'packetsize', 'type': 'I'},
    {'name': 'water_depth', 'type': 'f'},
    {'name': 'frequency', 'type': 'I'},
    {'name': '-', 'type': '28s'},
    {'name': 'gps_speed', 'type': 'f'},
    {'name': 'temperature', 'type': 'f'},
    {'name': 'lon_enc', 'type': 'i'},
    {'name': 'lat_enc', 'type': 'i'},
    {'name': 'water_speed', 'type': 'f'},
    {'name': 'course', 'type': 'f'},
    {'name': 'altitude', 'type': 'f'},
    {'name': 'heading', 'type': 'f'},
    {'name': 'flags', 'type': 'H'},
    {'name': '-', 'type': '6s'},
    {'name': 'time1', 'type': 'I'},
    # {'name': '-', 'type': '40s'}
)

F2_FLAGS = {
    'has_altitude':    0x0200,
    'has_heading':     0x0100,
    'has_track':       0x0080,
    'has_water_speed': 0x0040,
    'has_position':    0x0010,
    'has_packet':      0x0008,
    'has_temperature': 0x0004,
    'has_gps_speed':   0x0002,
}

F3_FLAGS = {
    'has_altitude':    0x0200,
    'has_heading':     0x0100,
    #
    'has_track':       0x0080,
    'has_water_speed': 0x0040,
    'has_position':    0x0010,
    #
    'has_tbd1':      0x0008,
    'has_temperature': 0x0004,
    'has_gps_speed':   0x0002,
    #
}


FRAME_DEFINITIONS = (
    F0_FRAME,
    F1_FRAME,
    F2_FRAME,
    F3_FRAME,
)


def build_pattern(fdef):
    return "<" + "".join(map(lambda x: x['type'], fdef))


def build_names(fdef):
    return list(map(lambda x: x['name'],
                filter(lambda x: x['name'] != '-', fdef)))


"""struct patterns for each format"""
FRAME_FORMATS = (
    build_pattern(FRAME_DEFINITIONS[0]),
    build_pattern(FRAME_DEFINITIONS[1]),
    build_pattern(FRAME_DEFINITIONS[2]),
    build_pattern(FRAME_DEFINITIONS[3]),
)

FLAG_FORMATS = (
    None,
    None,
    F2_FLAGS,
    F3_FLAGS,
)

"""fieldnames for each format"""
FRAME_FIELDS = (
    build_names(FRAME_DEFINITIONS[0]),
    build_names(FRAME_DEFINITIONS[1]),
    build_names(FRAME_DEFINITIONS[2]) + list(FLAG_FORMATS[2].keys()),
    build_names(FRAME_DEFINITIONS[3]) + list(FLAG_FORMATS[3].keys()),
)


CALCULATED_FIELDS = ['gps_speed_kph', 'longitude', 'latitude', 'water_depth_m', 'headersize', 'heading_deg']
