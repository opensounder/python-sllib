import unittest
from os import path
import sllib


class TestReaderSlg(unittest.TestCase):
    def setUp(self):
        self.dirname = path.dirname(path.abspath(__file__))
        self.path_small = path.join(self.dirname,
                                    'sample-data-lowrance',
                                    'other', 'small.slg')

    def test_header_slg(self):
        with sllib.create_reader(self.path_small) as reader:
            assert reader
            header = reader.header
            assert header
            assert header.format == 1
            assert header.version == 0
            assert header.framesize == 1200

    def test_enumerate_slg(self):
        with sllib.create_reader(self.path_small) as reader:
            count = 0
            last_time = 0
            first = True
            for frame in reader:
                if first:
                    print(frame)
                    first = False
                count = count + 1
                # self.assertGreaterEqual(frame.flags, 0)
                self.assertIn(frame.headerlen, [48, 52])
                if frame.flags & 0x0001 == 0:
                    # if bit is set then some kind of epoc
                    self.assertGreaterEqual(frame.time1, last_time)
                    last_time = frame.time1

                # test positions
                if frame.altitude < 0:
                    self.assertEqual(frame.altitude, -10000.0)
                else:
                    self.assertGreaterEqual(frame.altitude, 0)
                    self.assertLessEqual(frame.altitude, 300)
                # self.assertGreaterEqual(frame.longitude, 10)
                # self.assertLessEqual(frame.longitude, 15, "bad longitude in frame %d" % (count,))
                # self.assertGreaterEqual(frame.latitude, 50, "bad latitude in frame %d" % (count,))
                # self.assertLessEqual(frame.latitude, 60)

            self.assertEqual(count, 4789)
