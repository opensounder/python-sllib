import unittest
from os import path
import sllib


class TestReaderSl3(unittest.TestCase):
    def setUp(self):
        self.dirname = path.dirname(path.abspath(__file__))

        self.path_sl3 = path.join(self.dirname,
                                  'sample-data-lowrance', 'other',
                                  'sonar-log-api-testdata.sl3')

    def test_header_sl3(self):
        with sllib.create_reader(self.path_sl3) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 3
            assert header.version == 1
            assert header.framesize == 3200

    # def test_next(self):
    #     with sllib.create_reader(self.path_sl3) as reader:
    #         x = next(reader)
    #         assert x
    #         assert x.offset == 8
    #         # assert x.framesize == 3216
    #         # assert x.previous_framesize == 0
    #         # assert x.channel == 0
    #         # assert x.frame_index == 0
    #         assert x.upper_limit == 0.0
    #         assert x.lower_limit == 0.0
    #         # TODO: created_at
    #         # assert x.packetsize == 3072
    #         # assert x.water_depth == 6.622000217437744
    #         assert x.frequency == 0
    #         assert x.gps_speed == 2.585312843322754
    #         assert x.temperature == 19.350006103515625
    #         assert x.lon_enc == 1383678
    #         assert x.lat_enc == 8147302
    #         assert x.water_speed == 0
    #         assert x.course == 3.7873644828796387
    #         assert x.altitude == 118.89765930175781
    #         assert x.heading == 0
    #         assert x.flags == 702  # TODO: Validate this!!!
    #         assert x.time1 == 5
    #         assert x.previous_primary_offset == 8
    #         assert x.previous_secondary_offset == 0
    #         assert x.previous_downscan_offset == 0
    #         assert x.previous_left_sidescan_offset == 0
    #         assert x.previous_right_sidescan_offset == 0
    #         assert x.previous_composite_sidescan_offset == 0
    #         assert x.previous_dc_offset == 0
