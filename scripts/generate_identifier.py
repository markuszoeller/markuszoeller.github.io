#!/usr/bin/env python

import random
import string

N = 7

pool = string.letters + string.digits
print(''.join(random.choice(pool) for i in xrange(N)))
