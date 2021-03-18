from unittest import TestCase

from btfix.convertor import _convert_key, _convert_rand, _convert_ediv, _convert_device_mac


class ConvertorTestCase(TestCase):

    def test_convert_key(self):
        keys = [
            ('42,cf,98,31,2f,91,01,b6,a7,24,06,02,04,7f,ab,59', '42CF98312F9101B6A7240602047FAB59'),
            ('21,8a,dc,0e,b4,cb,18,60,e4,80,db,b1,bf,28,f3,87', '218ADC0EB4CB1860E480DBB1BF28F387'),
            ('8b,54,ff,13,6b,cc,91,3b,3f,a2,2b,88,a7,f0,c8,86', '8B54FF136BCC913B3FA22B88A7F0C886'),
        ]

        for key, expected in keys:
            self.assertEqual(expected, _convert_key(key))

    def test_convert_rand(self):
        rands = [
            ('ab,bc,cd,ef', '4023237803'),
            ('8a,0b,ac,8f,c9,9b,db,ea', '16923291314775919498'),
            ('ff,ee,dd,cc,bb,aa', '187723572702975'),
        ]

        for erand, expected in rands:
            self.assertEqual(expected, _convert_rand(erand))

    def test_convert_ediv(self):
        edivs = [
            ('00005cda', '23770'),
            ('abcdef', '11259375'),
            ('ffddcc', '16768460'),
        ]

        for ediv, expected in edivs:
            self.assertEqual(expected, _convert_ediv(ediv))

    def test_convert_device_mac(self):
        self.assertEqual(_convert_device_mac('e5d79a5c3d42'), 'E5:D7:9A:5C:3D:42')

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            _convert_rand('invalid input')
        with self.assertRaises(ValueError):
            _convert_ediv('invalid input')
