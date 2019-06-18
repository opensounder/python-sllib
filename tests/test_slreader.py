import unittest

import sllib


class TestSlReader(unittest.TestCase):
    def test_header(self):
        reader = sllib.create_reader("./sample-data-lowrance/Elite_4_Chirp/small.sl2")
        assert reader
        header = reader.header
        assert header
        assert header.format == 2
        assert header.version == 1
        assert header.blocksize == 1800

    def test_next(self):
        with sllib.create_reader("./sample-data-lowrance/Elite_4_Chirp/small.sl2") as reader:
            assert reader
            count = 0
            for block in reader:
                count = count + 1
                assert block
            assert count == 1
