import os
import unittest
from os import path
import sllib


class TestReaderSl3(unittest.TestCase):
    def setUp(self):
        self.dirname = path.dirname(path.abspath(__file__))

        self.path_sl3 = path.join(self.dirname,
                                  'sample-data-lowrance', 'other',
                                  'sonar-log-api-testdata.sl3')
        self.path_sl3_v2 = path.join(
            self.dirname, 'sample-data-lowrance', 'other',
            'format3_version2.sl3')

    def test_header_sl3(self):
        with sllib.create_reader(self.path_sl3) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 3
            assert header.version == 1
            assert header.framesize == 3200
            fields = reader.fields
            self.assertIn('channel', fields)

    def test_first(self):
        with sllib.create_reader(self.path_sl3, True) as reader:
            header = reader.header
            self.assertEqual(header.format, 3)
            x = next(reader)
            assert x
            assert x.offset == 8
            self.assertEqual(x.framesize, 2732, 'bad framesize')
            # print(x.to_dict(format=3))

            self.assertAlmostEqual(x.upper_limit, 98.4, 2)
            assert x.lower_limit == 0.0

            assert x.frequency == 0
            self.assertAlmostEqual(x.gps_speed, 2.25, 2)
            self.assertAlmostEqual(x.temperature, 2.3, 1)
            # assert x.temperature == 19.350006103515625
            self.assertAlmostEqual(x.longitude, 36.486296, 4)
            self.assertAlmostEqual(x.latitude, 56.5952053, 4)
            assert x.water_speed == 0
            # self.assertAlmostEqual(x.course, 288.83, 1)
            # assert x.altitude == 118.89765930175781
            # self.assertAlmostEqual(x.altitude, 118, 1)
            self.assertAlmostEqual(x.heading_deg, 78.98, 1)
            self.assertEqual(x.flags, 950)  # TODO: Validate !!!

    def test_read_all_v1(self):
        with sllib.create_reader(self.path_sl3, True) as reader:
            header = reader.header
            self.assertEqual(header.format, 3)
            self.assertEqual(header.version, 1)
            count = 0
            goodCount = 0

            box = {
                'lon': {'min': 36.48355597526586, 'max': 36.48649433485548},
                'lat': {'min': 56.59505156603242, 'max': 56.59533938054592},
                'depth': {'min': 3.0, 'max': 13.0}
            }
            for frame in reader:
                count += 1
                if frame.has_tbd1:
                    goodCount += 1
                # space
                self.assertGreaterEqual(frame.longitude, box['lon']['min'])
                self.assertLessEqual(frame.longitude, box['lon']['max'])
                self.assertGreaterEqual(frame.latitude, box['lat']['min'])
                self.assertLessEqual(frame.latitude, box['lat']['max'])
                self.assertGreaterEqual(frame.water_depth_m, box['depth']['min'])
                self.assertLessEqual(frame.water_depth_m, box['depth']['max'])

                # channels
                self.assertLessEqual(frame.channel, 9)
                self.assertLessEqual(frame.frequency, 10)

            self.assertEqual(count, 10124, 'wrong number of frames')
            self.assertEqual(goodCount, 7626, 'wrong number of frames with flag set')

            filesize = os.path.getsize(self.path_sl3)
            self.assertEqual(reader.tell(), filesize)

    def test_read_all_v2(self):
        filename = self.path_sl3_v2
        with sllib.create_reader(filename, strict=True) as reader:
            header = reader.header
            self.assertEqual(header.format, 3)
            self.assertEqual(header.version, 2)
            count = 0
            goodCount = 0

            box = {
                'lon': {'min': -91.2444, 'max': -91.24243771237497},
                'lat': {'min': 29.654006, 'max': 29.657156827530574},
                'depth': {'min': 3.0, 'max': 13.0}
            }
            for frame in reader:
                count += 1
                if frame.channel <= 5:
                    goodCount += 1
                # space
                self.assertGreaterEqual(frame.longitude, box['lon']['min'])
                self.assertLessEqual(frame.longitude, box['lon']['max'])
                self.assertGreaterEqual(frame.latitude, box['lat']['min'])
                self.assertLessEqual(frame.latitude, box['lat']['max'])
                # self.assertGreaterEqual(frame.water_depth_m, box['depth']['min'])
                # self.assertLessEqual(frame.water_depth_m, box['depth']['max'])

                # channels
                self.assertLessEqual(frame.channel, 9)
                self.assertLessEqual(frame.frequency, 10)

            self.assertEqual(count, 32768)
            self.assertEqual(goodCount, 16384)

            filesize = os.path.getsize(filename)
            self.assertEqual(reader.tell(), filesize)

    def test_filter_channels(self):
        with sllib.create_reader(self.path_sl3_v2) as reader:
            reader.add_filter(channels=[9])
            for frame in reader:
                self.assertEqual(frame.channel, 9)

        with sllib.create_reader(self.path_sl3_v2) as reader:
            reader.add_filter(channels=[1, 9])
            for frame in reader:
                self.assertIn(frame.channel, [1, 9])

    def test_filter_flags(self):
        with sllib.create_reader(self.path_sl3_v2) as reader:
            reader.add_filter(flags=702)
            count = 0
            for frame in reader:
                self.assertEqual(frame.flags, 702)
                count += 1

        self.assertEqual(count, 28672)
