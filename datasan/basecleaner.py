"""
A base class for validating and transforming records.
"""
# XXX: do we need an abort if any errors?


### IMPORTS

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from builtins import str
from past.builtins import basestring
from builtins import object

from .utils import all_vals_within


### CONSTANTS & DEFINES

UNKNOWN_REC_ID = '<unknown>'


### CODE ###

class BaseCleaner (object):
	rules = (
		# fxn or name
	)

	def __init__ (self, exclude_errors=False, id_fld=None, null_vals=[None, '']):
		# do we exclude records with errors?
		self.exclude_errors = exclude_errors
		# by default, what tdo we call a null value
		self.null_vals = null_vals
		# how do we extract an id from the record: literal fieldname or function?
		if isinstance (id_fld, basestring):
			self.message ("Extracting record id as '%s'" % id_fld)
			self.id_fxn = lambda x: x.get (id_fld, UNKNOWN_REC_ID)
		elif hasattr (id_fld, '__call__'):
			self.message ("Extracting record id with supplied function")
			self.id_fxn = id_fld
		else:
			self.message ("No record id extraction available")
			self.id_fxn = lambda x: 'unknown'

	def clean (self, recs):
		"""
		Clean an individual record by running every rule across it.

		Args:
			recs (seq): a list of records to be processed

		Returns:
			a list of produced records and a list of errors

		"""
		## Main:
		# storage for output
		errors = []
		proc_recs = []

		# for each record
		for i, r in enumerate (recs):
			rec_id = self.id_fxn (r)
			self.message ("Processing record index %s (id '%s')" % (i, rec_id))
			new_rec, errs = self.clean_rec (r)
			# TODO: exclude message
			if errs:
				self.message ("Cleaning failed")
				for e in errs:
					e['index'] = i
					e['id'] = rec_id
				errors.extend (errs)

			proc_recs.append (new_rec)
		self.message ("Cleaning finished", progress=False)

		## Postconditions & return:
		return proc_recs, errors

	def clean_rec (self, r):
		"""
		Clean an individual record by running every rule across it.

		Args:
			r (dict): a record to be processed

		Returns:
			a new record with the output and a list of errors

		"""
		# new rec to store info in & assoc errors
		new_rec = {}
		errors = []

		self.pre_process (r, new_rec)

		for cr in self.rules:
			# get values from the source fields
			vals = cr.get_src_vals_from_rec (r)

			# abort all vals are in cleaner or rule nulls
			if all_vals_within (vals, self.null_vals):
				continue

			if cr.are_vals_skippable (vals):
				continue

			# otherwise process through san chain
			try:
				out_vals = cr.process_vals (vals)
				# if we make it here, store it in new rec
				dst_flds = cr.dst_flds
				for df in dst_flds:
					new_rec[df] = out_vals
			except Exception as err:
				validation_msg = 'Validation failed: %s' % err
				errors.append ({
						'error': err,
						'values': list (vals),
						'fields': cr.get_src_flds_str(r),
					}
				)

		self.post_process (r, new_rec)

		## Postconditions & return:
		return new_rec, errors

	def message (self, msg, progress=True):
		print ('%s%s' % (msg, ' ...' if progress else '.'))

	def pre_process (self, old_rec, new_rec):
		# XXX: override in derived classes if necessary
		# handle errors
		pass

	def post_process (self, old_rec, new_rec):
		# XXX: override in derived classes if necessary
		# handle errors
		pass


### END ###
