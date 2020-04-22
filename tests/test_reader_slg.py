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
            for frame in reader:
                count = count + 1
                self.assertGreater(frame.offset, 0)
            self.assertEqual(count, 187)
