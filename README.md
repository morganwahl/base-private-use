# base-private-use
Encode arbitrary bits to a sequence of private-use codepoints.

[![CircleCI](https://circleci.com/gh/morganwahl/base-private-use.svg?style=svg)](https://circleci.com/gh/morganwahl/base-private-use)
[![codecov](https://codecov.io/gh/morganwahl/base-private-use/branch/master/graph/badge.svg)](https://codecov.io/gh/morganwahl/base-private-use)
[![Build Status](https://travis-ci.org/morganwahl/base-private-use.svg?branch=master)](https://travis-ci.org/morganwahl/base-private-use)
[![Coverage Status](https://coveralls.io/repos/github/morganwahl/base-private-use/badge.svg?branch=master)](https://coveralls.io/github/morganwahl/base-private-use?branch=master)

Fit 280 bytes of data into a tweet!

Most systems will leave private-use characters unmolested, as they should. This codec allows encoding arbitrary bits into a sequence of private-use codepoints, and back again.

The API is slightly awkward because it supports _bits_ that aren't necessarily byte-padded.

```py
import base_private

codepoints = base_private.encode(a_bunch_of_bytes, number_of_bits_i_care_about)

original_bytes, number_of_bits = base_private.decode(codepoints)
```
