#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='logzero',
    version='1.5.0',
    description="Robust and effective logging for Python 2 and 3",
    long_description=readme + '\n\n' + history,
    author="Chris Hager",
    author_email='chris@linuxuser.at',
    url='https://github.com/metachris/logzero',
    packages=find_packages(include=['logzero']),
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='logzero',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require={
        ':sys_platform=="win32"': ['colorama']
    }
)
