#!/usr/bin/env python

"""setuptools Setup script."""

from setuptools import setup
#from distutils.core import setup

setup(name='Champlitte',
    version      = '0.1',
    description  = 'Managing the Champlitte mass-upload to Wikimedia Commons.',
    py_modules = ['Record', 'RecordsProcessing', 'Task', 'UnicodeCSV'],
    author       = 'Jean-Frederic',
    author_email = 'JeanFred@github',
    license      = 'GPL')
