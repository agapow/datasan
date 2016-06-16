"""
Various general sanitizing functions.

Remember, the general form of a sanitzing function is to accept a value or
values, throw an exception if there's a problem and return a value (or values)
otherwise.

"""
# XXX: for_each, for_one?


### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import super
from builtins import str
from builtins import object


import re
import datetime

__all__ = [
	'FilterIf',
	'filter_non_nulls',
	'count',
	'JoinWith',
	'FromValues',
	'NotFromValues',
	'is_non_null'
	'DatetimeStrtoObj',
	'DatetimeObjToStr',
	'IfElse',
	'Const',
]


### CONSTS & DEFINES

WSPACE_RE = re.compile ('\s+')


### CODE ###

## Filtering & condensing sequences

class FilterIf (object):
	"""Filter out a list depending on value."""
	def __init__ (self, filter_fxn):
		self.filter_fxn = filter_fxn

	def __call__ (self, x):
		return [y for y in x if self.filter_fxn (y)]


class FilterIfEqual (FilterIf):
	def __init__ (self, keep_val):
		super (FilterIf, self).__init__ (lambda x: x == keep_val)


def filter_non_nulls (v):
	san = FilterIf (lambda x: x not in ['', None])
	return san (v)


def count (v):
	return len (list (v))


## Joining sequences

class JoinWith (object):
	"""Join a list of values together."""
	def __init__ (self, join_str):
		self.join_str = join_str

	def __call__ (self, x):
		return join_str.join ([str (y) for y in list(x)])


## Testing memebership

class FromValues (object):
	"""Check that this value falls within a given set of values"""
	def __init__ (self, val_list):
		self.val_list = val_list

	def __call__ (self, x):
		assert x in self.val_list, "value not in list '%s'" % ', '.join ([str(v) for v in self.val_list])
		return x


class NotFromValues (object):
	"""Check that this value doesn't fall within a given set of values"""
	def __init__ (self, val_list):
		self.val_list = val_list

	def __call__ (self, x):
		assert x not in self.val_list, "value in list '%s'" % ', '.join ([str(v) for v in self.val_list])
		return x


def is_non_null (v):
	"""Check that this value isn't null (none or a blank string)"""
	san = NotFromValues ([None, ''])
	return san (v)


## Date & time conversion

class DatetimeStrtoObj (object):
	"""Convert a formatted datetime string into a formatted object"""
	def __init__ (self, fmt):
		self.fmt = fmt

	def __call__ (self, v):
		# scrub excess whitespace
		v = v.strip()
		v = WSPACE_RE.sub (' ', v)
		return datetime.datetime.strptime (v, self.fmt)


class DatetimeObjToStr (object):
	"""Convert a datetime object into a formatted string"""
	def __init__ (self, fmt):
		self.fmt = fmt

	def __call__ (self, v):
		return v.strftime (self.fmt)



## Conditionals

class IfElse (object):
	"""Transform values conditionally"""
	# XXX: be nice if it accepts lists of sanitiziers but more complex
	def __init__ (self, cond_fxn, if_sans, else_sans=None):
		self.cond_fxn = cond_fxn
		self.if_sans = if_sans
		self.else_sans = else_sans

	def __call__ (self, x):
		if self.cond_fxn (v):
			return self.if_sans (v)
		else:
			if self.else_sans:
				return self.else_sans (v)
			else:
				return v


class Const (object):
	"""Return a constant value"""
	def __init__ (self, const):
		self.const = const

	def __call__ (self, v):
		return self.const


## Mappings and translations

class MapVal (object):
	"""Return a constant value"""
	def __init__ (self, mapping, default=None, transform_fxn=None):
		self.mapping = mapping
		self.default = default
		ret_self_fxn = lambda x: x
		self.transform_fxn = transform_fxn or ret_self_fxn

	def __call__ (self, v):
		return self.mapping.get (self.transform_fxn (v), self.default)


class GenericTrueFalseMap (MapVal):
	def __init__ (self, default=None):
		true_vals = ('true', 't', 'on', '1', '+', 'positive', 'pos', 'yes', 'y')
		false_vals = ('false', 'f', 'off', '0', '-', 'negative', 'neg', 'no', 'n')
		mapping = {}
		for x in true_vals:
			mapping[x] = True
		for x in false_vals:
			mapping[x] = False
		super (GenericTrueFalseMap, self).__init__ (
			mapping,
			default=default,
			transform_fxn=lambda x: str(x).lower(),
		)


class TrueFalseTo (object):
	"""Convert true-false to another value"""
	def __init__ (self, true_val, false_val, other_val=None):
		self.true_val = true_val
		self.false_val = false_val
		self.other_val = other_val

	def __call__ (self, v):
		if v is True:
			return self.true_val
		elif v is False:
			return self.false_val


class MapSingleVal (object):
	"""Convert specific value to a constant"""
	def __init__ (self, from_val, to_val):
		self.from_val = from_val
		self.to_val = to_val

	def __call__ (self, x):
		if v == self.from_val:
			return self.to_val
		else:
			return v


### END ###
