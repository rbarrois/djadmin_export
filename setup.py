#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is distributed under the LGPLv3+ license.
# Copyright (c) Raphaël Barrois

import codecs
import os
import re
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command import build_py

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


def clean_readme(fname):
    """Cleanup README.rst for proper PyPI formatting."""
    with codecs.open(fname, 'r', 'utf-8') as f:
        return ''.join(
            re.sub(r':\w+:`([^`]+?)( <[^<>]+>)?`', r'``\1``', line)
            for line in f
            if not (line.startswith('.. currentmodule') or line.startswith('.. toctree'))
        )


class BuildWithMakefile(build_py.build_py):
    """Custom 'build' command that runs 'make build' first."""
    def run(self):
        subprocess.check_call(['make', 'build'])
        if sys.version_info[0] < 3:
            # Under Python 2.x, build_py is an old-style class.
            return build_py.build_py.run(self)
        return super().run()


PACKAGE = 'djadmin_export'


setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    author="Raphaël Barrois",
    author_email="raphael.barrois+%s@polytechnique.org" % PACKAGE,
    description="Export functions for Django admin",
    long_description=clean_readme('README.rst'),
    license="LGPLv3+",
    keywords=['Django', 'admin', 'export'],
    url="http://github.com/rbarrois/djadmin_export",
    download_url="http://pypi.python.org/pypi/djadmin_export/",
    packages=find_packages(exclude=['dev', 'tests*']),
    setup_requires=[
        'setuptools>=0.8',
    ],
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    test_suite='tests',
    zip_safe=False,  # Prevent distribution as eggs for South.
)
