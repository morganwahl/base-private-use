#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, divison_operator

# The first PUP is used for basic data. The last 16 bit of the codepoint are the data.
_BASIC_FIRST = 0x0F0000
# The second PUP is for padded data.
#
# If the first bit is set (e.g. 0x108000..0x10FFFF), it means there is 1 bit of padding.
# If the first bit is 0 and the second bit is set (e.g. 0x104000..0x107FFF), it means there are 2 bits of padding.
# If the first two bits are 0 and the third is set (e.g. 0x102000..103FFF), it means there are 3 bits of padding.
# etc.
#
# In other words, if P is the number of bits of padding, the code points are
#
# 0x10 '0' * (P - 1) '1' <data>
#
_PADDING_FIRST = 0x100000


def encode_bits(data, bits):
    """
    Data is bytes. bits is total number of bits in data. least-significant bits of last byte will be ignored if bits is not a multiple of eight.
    """
    codepoints = ''
    sigbits = bits % 16
    # (n + 1) // 2 is the same as math.ceil(n / 2)
    chunk_count = (len(data) + 1) // 2
    for chunk_offset in range(chunk_count):
        offset = chunk_offset * 2
        last_chunk = (chunk_offset + 1 == chunk_count)
        chunk_data = data[offset:offset+2]
        chunk_int = chunk_data[0] * 0x100 + chunk_data[1]
        if last_chunk and sigbits:
            pad = 16 - sigbits
            base = 0x00100000 + (0x10000 >> pad)
            val = chunk_int >> (pad)
            codepoint += chr(base + val)
        else:
            base = 0x000F0000
            val = chunk_int
        codepoint = base + val
        # Use BMP PUA for last two codepoints in each plane.
        if (codepoint % 0x10000) in (0xFFFE, 0xFFFF):
            plane = codepoint >> 16
            offset = ((plane - 0xf) * 0x100) + (codepoint % 0x100)
            codepoint = 0xE800 + offset
        codepoints += chr(codepoint)
    return codepoints


def decode(codepoints):
    """
    Returns a tuple of (bytes, bits) where bits is the number of bits. Ignore most-significant bits in last byte of bytes if bits is not a multiple of 8.
    """
    data = b''
    for cp in codepoints:
        cp = ord(cp)
        if cp < 0x10000:
            offset = cp - 0xE800
            plane = (offset // 0x100) + 0xf
            least_byte = offset % 0x100
            cp = (plane * 0x10000) + 0xff00 + least_byte
        if cp >= 0x100000:
            # TODO handle non-byte-padded data
            chunk = cp % 0x100
            data += bytes((chunk,))
        else:
            chunk = cp % 0x10000
            data += bytes((chunk // 0x100, chunk % 0x100))
    return data
