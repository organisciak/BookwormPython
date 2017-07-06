#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='bwypy',
      version='1.0',
      description='Bwypy: Python Tools for Bookworm',
      author='Peter Organisciak',
      author_email='organisciak@gmail.com',
      url='http://bookworm.htrc.illinois.edu',
      keywords='hathitrust text-mining text-analysis bookworm',
      license='NCSA',
      packages=find_packages(),
      install_requires=['pandas', "ujson"]
      )
