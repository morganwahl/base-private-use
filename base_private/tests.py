from __future__ import unicode_literals

import unittest

from hypothesis import given
from hypothesis.strategies import binary

from base_private import decode, encode


class AlgoritmTest(unittest.TestCase):
    def test_encode(self):
        for bits, encoded in (
                (b'\x00\x00', '\U000F0000'),
                (b'\x00', '\U00100100'),
                (b'\xff\xfe', '\ue8fe'),
                (b'\xff\xff', '\ue8ff'),
                (b'\xfe', '\U001001FE'),
                (b'\xff', '\U001001FF'),
        ):
            with self.subTest(bits=bits):
                self.assertEqual(encode(bits), encoded)

    def test_decode(self):
        for codepoints, decoded in (
                ('', b''),
                ('\U000F0000', b'\x00\x00'),
                ('\U00100100', b'\x00'),
                ('\ue8fe', b'\xff\xfe'),
                ('\ue8ff', b'\xff\xff'),
        ):
            with self.subTest(codepoints=codepoints):
                self.assertEqual(decode(codepoints), decoded)


class PropertiesTest(unittest.TestCase):
    @given(binary())
    def test_roundtrip(self, bits):
        print(bits)
        self.assertEqual(
            bits,
            decode(encode(bits)),
        )
