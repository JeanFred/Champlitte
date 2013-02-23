#!/usr/bin/env python

"""setuptools Setup script."""

from setuptools import setup
#from distutils.core import setup

setup(name='Champlitte',
    version      = '0.1',
    description  = 'Managing the Champlitte mass-upload to Wikimedia Commons.',
    author       = 'Jean-Frederic',
    author_email = 'JeanFred@github',
    packages     = [''],
    license      = 'GPL',
    install_requires = ['MassUploadLibrary'],
    dependency_links = ['https://github.com/JeanFred/MassUploadLibrary/archive/master.tar.gz#egg=MassUploadLibrary'],
    )