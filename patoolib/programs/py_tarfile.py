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
"""Archive commands for the tarfile Python module."""
from patoolib import util
import tarfile

READ_SIZE_BYTES = 1024*1024


def list_tar (archive, compression, cmd, **kwargs):
    """List a TAR archive with the tarfile Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('listing %s...' % archive)
    tfile = tarfile.open(archive)
    try:
        tfile.list(verbose=verbose)
    finally:
        tfile.close()
    return None

test_tar = list_tar

def extract_tar (archive, compression, cmd, **kwargs):
    """Extract a TAR archive with the tarfile Python module."""
    verbose = kwargs['verbose']
    outdir = kwargs['outdir']
    if verbose:
        util.log_info('extracting %s...' % archive)
    tfile = tarfile.open(archive)
    try:
        tfile.extractall(path=outdir)
    finally:
        tfile.close()
    if verbose:
        util.log_info('... extracted to %s' % outdir)
    return None


def create_tar (archive, compression, cmd, *args, **kwargs):
    """Create a TAR archive with the tarfile Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('creating %s...' % archive)
    mode = get_tar_mode(compression)
    tfile = tarfile.open(archive, mode)
    try:
        for filename in args:
            tfile.add(filename)
    finally:
        tfile.close()
    return None


def get_tar_mode (compression):
    """Determine tarfile open mode according to the given compression."""
    if compression == 'gzip':
        return 'w:gz'
    if compression == 'bzip2':
        return 'w:bz2'
    if compression:
        msg = 'pytarfile does not support %s for tar compression'
        util.log_error(msg % compression)
    # no compression
    return 'w'
