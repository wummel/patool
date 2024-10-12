#!/usr/bin/env python
# Copyright (C) 2010-2023 Bastian Kleineidam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Setup file for building, packaging and distributing this software."""

import sys

if not hasattr(sys, "version_info") or sys.version_info < (3, 10, 0, "final", 0):
    raise SystemExit("This program requires Python 3.10 or later.")
import os

from setuptools import setup


def read_configdata(basedir):
    """Read package meta data from configuration module."""
    configdata = {}
    configdata_py = os.path.join(basedir, "patoolib", "configuration.py")
    with open(configdata_py, encoding="utf-8") as f:
        exec(f.read(), configdata)
    return configdata


def read_readme(basedir):
    """Get contents of the README.md file."""
    readme_md = os.path.join(basedir, "README.md")
    with open(readme_md, encoding="utf-8") as f:
        return f.read()


basedir = os.path.abspath(os.path.dirname(__file__))
configdata = read_configdata(basedir)
readme = read_readme(basedir)


setup(
    name=configdata["AppName"],
    version=configdata["Version"],
    description=configdata["Description"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=configdata["Author"],
    author_email=configdata["AuthorEmail"],
    license=configdata["License"],
    url=configdata["Url"],
    python_requires=">=3.10",
    project_urls={
        "Source": "https://github.com/wummel/patool",
    },
    packages=['patoolib', 'patoolib.programs'],
    entry_points={
        'console_scripts': [
            'patool = patoolib.cli:main_cli',
        ]
    },
    keywords="archiver,archive,compression,commandline,manager",
    classifiers=[
        'Environment :: Console',
        'Topic :: System :: Archiving :: Compression',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
)
