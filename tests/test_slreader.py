import unittest
from os import path
import sllib


class TestSlReader(unittest.TestCase):
    def setUp(self):
        self.dirname = path.dirname(path.abspath(__file__))
        self.path_small = path.join(self.dirname,
                                    'sample-data-lowrance',
                                    'Elite_4_Chirp', 'small.sl2')
        self.path_v1 = path.join(self.dirname,
                                 'sample-data-lowrance', 'Elite_4_Chirp',
                                 'version-1.sl2')

    def test_header(self):
        with sllib.create_reader(self.path_small) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 2
            assert header.version == 0
            assert header.blocksize == 3200

        with sllib.create_reader(self.path_v1) as reader:
            assert reader
            assert reader.header.version == 1

    def test_next(self):
        with sllib.create_reader(self.path_small) as reader:
            x = next(reader)
            assert x
            assert x.offset == 8
            assert x.previous_primary_offset == 8
            assert x.previous_secondary_offset == 0
            assert x.previous_downscan_offset == 0
            assert x.previous_left_sidescan_offset == 0
            assert x.previous_right_sidescan_offset == 0
            assert x.previous_composite_sidescan_offset == 0
            assert x.blocksize == 3216
            assert x.previous_blocksize == 0
            assert x.packetsize == 3072
            assert x.frame_index == 0
            assert x.upper_limit == 0
            assert x.lower_limit == 19.600000381469727
            assert x.frequency == 8
            assert x.water_depth == 6.622000217437744
            assert x.keel_depth == 0
            assert x.gps_speed == 2.585312843322754
            assert x.temperature == 19.350006103515625
            assert x.lon_enc == 1383678
            assert x.lat_enc == 8147302
            assert x.water_speed == 0
            assert x.course == 3.7873644828796387
            assert x.altitude == 118.89765930175781
            assert x.heading == 0
            assert x.flags == 702  # TODO: Validate this!!!
            assert x.time1 == 5

    def test_enumerate(self):
        with sllib.create_reader(self.path_small) as reader:
            assert reader
            count = 0
            for block in reader:
                count = count + 1
                assert block
            assert count == 4017
