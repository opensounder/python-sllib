import unittest
from os import path
import sllib


def doframe(t: unittest.TestCase, curr: sllib.Frame, prev: sllib.Frame):
    """Validate some basic data for the frame"""
    t.assertGreaterEqual(curr.course, 0)
    t.assertLessEqual(curr.course, 6.28)
    t.assertLess(curr.gps_speed, 15)
    t.assertLess(curr.altitude, 500)
    t.assertLess(curr.temperature, 22)
    t.assertGreater(curr.temperature, 10)
    t.assertGreater(curr.framesize, curr.packetsize)
    t.assertGreater(curr.framesize, 1900)
    t.assertLessEqual(len(curr.packet), curr.packetsize)
    if prev is not None:
        t.assertGreater(curr.offset, prev.offset)
        t.assertGreaterEqual(curr.time1, prev.time1)


class TestReaderSl2(unittest.TestCase):
    def setUp(self):
        self.dirname = path.dirname(path.abspath(__file__))
        self.path_small = path.join(self.dirname,
                                    'sample-data-lowrance',
                                    'Elite_4_Chirp', 'small.sl2')
        self.path_v1 = path.join(self.dirname,
                                 'sample-data-lowrance', 'Elite_4_Chirp',
                                 'Chart 05_11_2018 [0].sl2')

        self.path_sl3 = path.join(self.dirname,
                                  'sample-data-lowrance', 'unknown',
                                  'sonar-log-api-testdata.sl3')

    def test_header_sl2(self):
        with sllib.create_reader(self.path_small) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 2
            assert header.version == 0
            assert header.framesize == 3200

        with sllib.create_reader(self.path_v1) as reader:
            assert reader
            assert reader.header.format == 2
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
            assert x.framesize == 3216
            assert x.previous_framesize == 0
            assert x.channel == 0
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
            prev = None
            for frame in reader:
                count = count + 1
                assert frame
                doframe(self, frame, prev)
                prev = frame
            assert count == 4017

    def test_next_v1(self):
        with sllib.create_reader(self.path_v1) as reader:
            x = next(reader)
            assert x
            assert x.offset == 8
            assert x.previous_primary_offset == 0
            assert x.previous_secondary_offset == 0
            assert x.previous_downscan_offset == 8
            assert x.previous_left_sidescan_offset == 0
            assert x.previous_right_sidescan_offset == 0
            assert x.previous_composite_sidescan_offset == 0
            assert x.framesize == 2064
            assert x.previous_framesize == 0
            assert x.channel == 2
            assert x.packetsize == 1920
            assert x.frame_index == 0
            assert x.upper_limit == 0
            assert x.lower_limit == 20.100000381469727
            assert x.frequency == 0
            assert x.water_depth == 7.406000137329102
            assert x.keel_depth == 0
            assert x.gps_speed == 0.6000000238418579
            assert x.temperature == 19.943925857543945
            assert x.lon_enc == 1373761
            assert x.lat_enc == 8163659
            assert x.water_speed == 0.6000000238418579
            assert x.course == 4.817108631134033
            assert x.altitude == 236.18765258789062
            assert x.heading == 0
            assert x.flags == 542  # TODO: Validate this!!!
            assert x.time1 == 99787

    def test_enumerate_v1(self):
        with sllib.create_reader(self.path_v1) as reader:
            assert reader
            count = 0
            prev = None
            for frame in reader:
                count = count + 1
                assert frame
                doframe(self, frame, prev)
                prev = frame
            assert count == 27458
