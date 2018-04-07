#!/usr/bin/env python

from distutils.core import setup

setup(
    name='metermonitor',
    version='0.0.1',
    description='Water meter monitor',
    long_description='See project page with usage examples at https://github.com/skhg/water_monitor',
    keywords='opencv iot',
    author='Jack Higgins',
    author_email='water_meter@jackhiggins.ie',
    url='https://github.com/skhg/water_monitor',
    packages=['metermonitor'],
    install_requires=[
    ],
    tests_require=[
        'mock',
        'nose',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'])
