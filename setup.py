#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Bastian Kleineidam
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
"""
Setup file for the distuils module.
"""

import sys
if not hasattr(sys, "version_info") or sys.version_info < (2, 4, 0, "final", 0):
    raise SystemExit("This program requires Python 2.4 or later.")
import os
from distutils.core import setup

AppName = "patool"
AppVersion = "0.5"
MyName = "Bastian Kleineidam"
MyEmail = "calvin@users.sourceforge.net"

data_files = []
if os.name == 'nt':
    data_files.append(('share', ['doc/patool.txt']))
else:
    data_files.append(('share/man/man1', ['doc/patool.1']))

setup (
    name = AppName,
    version = AppVersion,
    description = "simple manager for file archives of various types",
    author = MyName,
    author_email = MyEmail,
    maintainer = MyName,
    maintainer_email = MyEmail,
    license = "GPL",
    packages = ['patoolib', 'patoolib.programs'],
    data_files = data_files,
    scripts = ['patool'],
)
