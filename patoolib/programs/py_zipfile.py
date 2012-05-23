# -*- coding: utf-8 -*-
# Copyright (C) 2012 Bastian Kleineidam
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
"""Archive commands for the zipfile Python module."""
from patoolib import util
import zipfile
import os

READ_SIZE_BYTES = 1024*1024


def list_zip (archive, compression, cmd, **kwargs):
    """List member of a ZIP archive with the zipfile Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('listing %s...' % archive)
    zfile = zipfile.ZipFile(archive, "r")
    try:
        for name in zfile.namelist():
            util.log_info('member %s' % name)
    finally:
        zfile.close()
    return None

test_zip = list_zip

def extract_zip (archive, compression, cmd, **kwargs):
    """Extract a ZIP archive with the zipfile Python module."""
    verbose = kwargs['verbose']
    outdir = kwargs['outdir']
    if verbose:
        util.log_info('extracting %s...' % archive)
    zfile = zipfile.ZipFile(archive)
    try:
        zfile.extractall(outdir)
    finally:
        zfile.close()
    if verbose:
        util.log_info('... extracted to %s' % outdir)
    return None


def create_zip (archive, compression, cmd, *args, **kwargs):
    """Create a ZIP archive with the zipfile Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('creating %s...' % archive)
    zfile = zipfile.ZipFile(archive, 'w')
    try:
        for filename in args:
            if os.path.isdir(filename):
                write_directory(zfile, filename)
            else:
                zfile.write(filename)
    finally:
        zfile.close()
    return None


def write_directory (zfile, directory):
    """Write recursively all directories and filenames to zipfile instance."""
    for dirpath, dirnames, filenames in os.walk(directory):
        zfile.write(dirpath)
        for filename in filenames:
            zfile.write(os.path.join(dirpath, filename))
