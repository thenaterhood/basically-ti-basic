#!/usr/bin/env python

from setuptools import setup
import sys
import os

install_requires = [
    ]

test_requires = [
    ]

data_files=[]


setup(name='basically_ti_basic',
    version='0.1.1',
    description='Utilities for manipulating TI-Basic program files',
    author='Nate Levesque',
    author_email='public@thenaterhood.com',
    url='https://github.com/thenaterhood/basically-ti-basic/archive/master.zip',
    install_requires=install_requires,
    tests_require=test_requires,
    entry_points={
        'console_scripts': [
            'basically-ti-basic = basically_ti_basic.__main__:main',
            'tibc = basically_ti_basic.__main__:main'
        ]
    },
    test_suite='nose.collector',
    package_dir={'':'src'},
    packages=[
        'basically_ti_basic',
        'basically_ti_basic.compiler',
        'basically_ti_basic.files',
        'basically_ti_basic.tokens'
        ],
    data_files=data_files,
    package_data={
        }
    )
