import os
from sllib.errors import FieldNotFoundError, OffsetError
import unittest
from os import path
import sllib
from sllib import Reader, create_reader
from . import fixtures

BASE=path.join(path.dirname(path.abspath(__file__)), 'sample-data-lowrance')



class TestReader(unittest.TestCase):
    
    def test_formver_reader(self):
        stream = open(fixtures.SL2_SMALL, 'rb')
        reader = Reader(stream)
        self.assertEqual(reader.formver, (2,0))
        reader.close()
        s = f'{reader.header}'
        self.assertIn('<Header(format=2', s)


    def test_add_filter_fields(self):
        with create_reader(fixtures.SL2_SMALL) as reader:
            reader.add_filter(has_heading=True)

            count=0
            for frame in reader:
                count += 1
            
            self.assertEqual(count, 0, 'wrong number of frames returned')

    def test_add_filter_bad_field(self):
        with create_reader(fixtures.SL2_SMALL) as reader:
            with self.assertRaises(FieldNotFoundError):
                reader.add_filter(spam=True)

    def test_corrupt(self):
        with create_reader(fixtures.SL2_CORRUPT_PARTLY, strict=True) as reader:
            first = next(reader)
            self.assertEqual(first.offset, 8)

            with self.assertRaises(OffsetError):
                second = next(reader)
            #self.assertEqual(second.offset, 3224)
