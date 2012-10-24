#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is distributed under the LGPLv3+ license.
# Copyright (c) 2012 Raphaël Barrois

from setuptools import setup, find_packages
import os
import re

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    path_components = package_components + ['__init__.py']
    with open(os.path.join(root_dir, *path_components)) as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'djadmin_export'


setup(
    name="djadmin_export",
    version=get_version(PACKAGE),
    author="Raphaël Barrois",
    author_email="raphael.barrois@polytechnique.org",
    description="Export functions for Django admin",
    license="LGPLv3+",
    keywords=['Django', 'admin', 'export'],
    url="http://github.com/rbarrois/djadmin_export",
    download_url="http://pypi.python.org/pypi/djadmin_export/",
    packages=find_packages(),
    setup_requires=[
        'distribute',
    ],
    install_requires=[
        'Django>=1.3',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='tests',
)

