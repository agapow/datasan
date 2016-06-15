from setuptools import setup, find_packages
import sys, os

from datasan import __VERSION__

setup (
   name='datasan',
   version=__VERSION__,
   description="A framework for transforming and validating data records",
   long_description="""
A common data science is to remap or check a series of records. This package
offers a framework for this 'santizing' based on the following ideas:

* data is assumed to be fields in a record, treated as a dict
* validation and transformation are the same thing
* cleaning functions can be chained
* cleaning details are consistently and tersely written, to make the process documentable and understandable
   """,
   classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
   keywords='',
   author='Paul Agapow',
   author_email='p.agapow@imperial.ac.uk',
   url='',
   license='MIT',
   packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
   include_package_data=True,
   zip_safe=False,
   install_requires=[
   # -*- Extra requirements: -*-
   ],
   entry_points={},
)
