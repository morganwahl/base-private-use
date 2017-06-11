from __future__ import unicode_literals

import unittest

from base_private import encode

class AlgoritmTest(unittest.TestCase):
    def test(self):
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

        
