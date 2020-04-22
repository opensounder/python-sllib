import unittest
from os import path
import sllib


class TestSl3Reader(unittest.TestCase):
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
