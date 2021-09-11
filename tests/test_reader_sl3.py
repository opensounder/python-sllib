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

    def test_header_sl3(self):
        with sllib.create_reader(self.path_sl3) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 3
            assert header.version == 1
            assert header.framesize == 3200

    def test_first(self):
        with sllib.create_reader(self.path_sl3) as reader:
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

    def test_read_all(self):
        with sllib.create_reader(self.path_sl3) as reader:
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
                if frame.has_packet:
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

            self.assertEqual(count, 10124)
            self.assertEqual(goodCount, 7626)

            filesize = os.path.getsize(self.path_sl3)
            self.assertEqual(reader.tell(), filesize)
