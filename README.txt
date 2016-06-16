datasan
=======
A framework for sanitizing datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Introduction and background
---------------------------

Over the years, I've cleaned / munged / reshaped far too many datasets. While
every dataset was different, the general shape of the problem was always the
same: *take this set of records, for every record look at this field, do this to
it, look at the next field ...* For complex datasets, the transforming script
started to look like an indigestible mass of code, thwarting later attempts to
understand what it had done. What I needed was a more maintainable and standard
framework for transforming data, that took care of the boilerplate tasks, was
easy to read and reference, and provided (or made easy) common transformation
tasks.

Hence datasan, which provides:

* A framework for iterating over records and targeted fields in a record

* A simple way of designating a source field (or set of fields) and the chain of transformations they will require

* A simple idiom for transforming functions that will allow many existing functions to be used and more complex ones to be easily constructed from powerful base classes

* A rich library of sanitizing functions

You can use datasan at whatever level you like: the whole dataset cleaning level, chains of sanitizers for cleaning fields 

Using datasan
-------------

Assumptions and idioms
~~~~~~~~~~~~~~~~~~~~~~

Datasan makes a number of simplifying assumptions, not all of which will suit
everyone:

* A dataset is a sequence of records

* A record is a dictionary of field name / field value pairs

* Sanitizing data involves copying values from a source record to a new destination record

* Sanitizing data includes both transforming / changing / converting it and validating / checking it. Validation is simply passing through the unchanged value if it is correct. (This was the great insight of Ian Bicking in his FormEncode package which inspired this work.)

* Sanitizing is achieved by passing data through a chain of sanitizing functions, each accepting the output of the previous

The functionality of datasan is captured in a number of objects:

* A **sanitizer** is a function that accepts a value or values, trnasforming of validating them into a return value or values. If the transfromation or validation fails, it throws an error.

* A **chain** is source field or fields, a sequence of sanitizers they are to be run through, and a destination field, along with some customizable behaviour.

* A **cleaner** is a set of chains that can be run on a dataset.


__ (self, src_flds, sanitizers, dst_flds, required=False,
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




Credits and thanks
------------------

Ian Bicking's FormEncode package inspired the "chain of sanitzers" idea. Years ago, I wrote a package konval that captured these ideas. It's since been taken over by Peter Melias and gone in a different direction. Look at at ealry commits on the github repo to see how that worked.

Portions of this work were completed while I was funded by EU FP7 EUCLIDS and H2020 PERFORM grants.


References
----------

* `FormEncode <http://formencode.org>`__

* `konval on PyPi <http://pypi.python.org/pypi/konval>`__
