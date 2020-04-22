import unittest
import sllib


class TestFrame(unittest.TestCase):

    def test_to_dict(self):
        f = sllib.Frame(lon_enc=1383678, lat_enc=8147302, gps_speed=2.5)
        d = f.to_dict()
        assert d
        self.assertIn('gps_speed_kph', d)

    def test_gps_speed_kph(self):
        f = sllib.Frame(gps_speed=2.5)
        assert hasattr(f, 'gps_speed_kph')
        self.assertEqual(f.gps_speed_kph, 4.63)

    def test_location(self):
        f = sllib.Frame(lon_enc=1383678, lat_enc=8147302)
        assert hasattr(f, 'longitude')
        self.assertEqual(f.longitude, 12.471605890323259)
        self.assertEqual(f.latitude, 58.97372610987078)
