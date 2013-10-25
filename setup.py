#!/usr/bin/env python

"""setuptools Setup script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = []
requires = ['MassUploadLibrary']
dependency_links = ['https://github.com/JeanFred/MassUploadLibrary/archive/master.tar.gz#egg=MassUploadLibrary']
scripts  = []

setup(name='Champlitte',
    version      = '0.1',
    description  = 'Managing the Champlitte mass-upload to Wikimedia Commons.',
    author       = 'Jean-Frederic',
    author_email = 'JeanFred@github',
    url          = 'http://github.com.org/JeanFred/Champlitte',
    license      = 'MIT',
    packages         = packages,
    install_requires = requires,
    dependency_links = dependency_links,
)