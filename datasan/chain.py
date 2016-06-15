"""
A class for housing and managing a chain of transformations.
"""

# TODO: null_val is actually a function? allow for more sophisticated checks


### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object

from .utils import all_vals_within


### CONSTANTS & DEFINES

### CODE ###

def is_single_val (v):
	"""Is this a single value or a list of values?"""
	return not isinstance (v, (list, tuple))


class Chain (object):
	def __init__ (self, src_flds, sanitizers, dst_flds, required=False,
			def_val=None, null_val=None):
		"""
		C'tor for a transformation chain.

		Args:
			src_flds (str or seq): field names to extract values from
			sanitizers (sanitizer or seq): functions to transform values with
			dst_flds (str or seq): field names to fill with values
			required (bool): process the field if it is null anyway?
			def_val: value to return if the record doesn't possess it
			null_val: the missing / skip / don't process value

		"""
		self.src_flds = src_flds
		if sanitizers is None:
			self.sanitizers = []
		elif is_single_val (sanitizers):
			self.sanitizers = [sanitizers]
		else:
			self.sanitizers = sanitizers
		self.dst_flds = [dst_flds] if is_single_val (dst_flds) else dst_flds
		self.required = required
		self.def_val = def_val
		self.null_val = null_val

	def get_src_flds_str (self, rec):
		"""
		Return names of source fields.
		"""
		if is_single_val (self.src_flds):
			return self.src_flds
		else:
			return ', '.join (self.src_flds)

	def get_src_vals_from_rec (self, rec):
		"""
		Return the values for the source fields from a record.

		This extracts the values from the record, returning the default value
		if it cannot be found.
		"""
		if is_single_val (self.src_flds):
			return rec.get (self.src_flds, self.def_val)
		else:
			return [rec.get (f, self.def_val) for f in self.src_flds]

	def are_src_vals_null (self, vals):
		"""
		Are the source values all null?
		"""
		vals = list (vals)
		for v in vals:
			#if v not in self.null_val:
			if v not in [None, '']:
				return False
		print ('vals are null')
		return True

	def are_vals_skippable (self, vals):
		print (self.src_flds)
		if self.required:
			print ('required')
			return False
		else:
			self.are_src_vals_null (vals)

	def process_vals (self, vals):
		"""
		Feed values through the sanitizer chain.
		"""
		for s in self.sanitizers:
			vals = s (vals)
		return vals


### END ###
