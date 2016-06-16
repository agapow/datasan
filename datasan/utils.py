"""
Various utilities.
"""

### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import object
from builtins import str
from builtins import open
from future import standard_library
standard_library.install_aliases()

import argparse
import csv

__all__ = [
	'parse_clargs',
	'report_errors',
	'read_csv_as_dicts',
	'write_dicts_as_csv',
	'DataSanApp',
	'all_vals_within',
	'make_sequence',
]


### CONSTANTS & DEFINES

### CODE ###

def all_vals_within (search_vals, target_vals):
	"""
	Are the source values all null?
	"""
	search_vals = make_sequence (search_vals)
	for v in search_vals:
		if v not in target_vals:
			return False
	return True


def make_sequence (v):
	if not isinstance (v, (list, tuple)):
		return [v]
	else:
		return v



def parse_clargs (version=None):
	"""
	Parse commandline arguments in a useful, universal way.
	"""
	parser = argparse.ArgumentParser (
		description='Transfrom records',
		# version = "v%s" %  version or __VERSION__,
	)

	parser.add_argument ('-o', '--outfile', help='name of transformed file produced')
	parser.add_argument ('infile', help='file to be processed')

	clargs = parser.parse_args()
	if clargs.outfile == None:
		clargs.outfile = clargs.infile.replace ('.csv', '.transformed.csv')

	return clargs


def report_errors (errors):
	if len (errors):
		print ("%s errors encountered:" % len (errors))
		for e in errors:
			print (e)
			vals = e['values']
			val_str = ', '.join (vals) if type (vals) in (list, tuple) else str (vals)
			print ("- index %(index)s, id %(id)s: %(msg)s (fields '%(fields)s', values <%(vals)s>)" % {
					'index': e['index'],
					'id': e['id'],
					'fields': e['fields'],
					'msg': e['error'],
					'vals': val_str,
				}
			)


def read_csv_as_dicts (in_pth):
	with open (in_pth, 'rU') as in_hndl:
		rdr = csv.DictReader (in_hndl)
		return [r for r in rdr]


def write_dicts_as_csv (recs, out_pth, flds=None):
	if not flds:
		keys = []
		for r in recs:
			keys.extend (list (r.keys()))
		flds = sorted (set (keys))
	with open (out_pth, 'w') as out_hndl:
		wrtr = csv.DictWriter (out_hndl, fieldnames=flds)
		wrtr.writeheader()
		wrtr.writerows (recs)


class DataSanApp (object):
	# XXX: run method
	def __init__ (self, cleaner_cls):
		args = parse_clargs()
		in_recs = read_csv_as_dicts (args.infile)
		clnr = cleaner_cls()
		out_recs, errors = clnr.clean (in_recs)
		report_errors (errors)
		write_dicts_as_csv (out_recs, args.outfile)


### END ###
