"""
Various module-wide constants.

"""


### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import re

__all__ = [
	'TRUE_FALSE_DICT',
	'CANON_SPACE_RE',
]


### CONSTANTS & DEFINES

TRUE_STRS = [
	'TRUE',
	'T',
	'ON',
	'YES',
	'Y',
	'+',
	'1',
	1,
]

FALSE_STRS = [
	'FALSE',
	'F',
	'OFF',
	'NO',
	'N',
	'-',
	'0',
	0,
]

TRUE_FALSE_DICT = {}
for v in TRUE_STRS:
	TRUE_FALSE_DICT[v] = True
for v in FALSE_STRS:
	TRUE_FALSE_DICT[v] = False

CANON_SPACE_RE = re.compile (r'[\-_\s]+')


### IMPLEMENTATION ###

### END #######################################################################
