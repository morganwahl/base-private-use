#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

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


def encode(data):
    # TODO Handle non-byte-padded bit sequences.
    from io import BytesIO
    data = BytesIO(data)
    codepoints = ''
    while True:
        chunk = data.read(2)
        if len(chunk) == 2:
            base = _BASIC_FIRST
            chunk = (chunk[0] << 8) + chunk[1]
        elif len(chunk) == 1:
            base = _PADDING_FIRST
            chunk = 0x0100 + chunk[0]
        else:
            break
        codepoint = base + chunk
        # Use BMP PUA for last two codepoints in each plane.
        if (codepoint % 0x10000) in (0xFFFE, 0x0FFFF):
            plane = codepoint >> 16
            offset = ((plane - 0xf) * 0x100) + (codepoint % 0x100)
            codepoint = 0xE800 + offset
        codepoints += chr(codepoint)
    return codepoints


def decode(codepoints):
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


def main():
    import sys
    data = sys.argv[1].encode('utf-8')
    encoded = encode(data)
    roundtrip = decode(encoded)
    print(data, encoded, roundtrip, sep='\n')


if __name__ == '__main__':
    main()
