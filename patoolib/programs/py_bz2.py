# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Bastian Kleineidam
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
"""Archive commands for the bz2 Python module."""
from .. import util
try:
    # try external bz2file module with multi-stream support
    import bz2file as bz2
except ImportError:
    import bz2

READ_SIZE_BYTES = 1024*1024

def extract_bzip2 (archive, compression, cmd, **kwargs):
    """Extract a BZIP2 archive with the bz2 Python module."""
    verbose = kwargs['verbose']
    outdir = kwargs['outdir']
    if verbose:
        util.log_info('extracting %s...' % archive)
    targetname = util.get_single_outfile(outdir, archive)
    bz2file = bz2.BZ2File(archive)
    try:
        with open(targetname, 'wb') as targetfile:
            data = bz2file.read(READ_SIZE_BYTES)
            while data:
                targetfile.write(data)
                data = bz2file.read(READ_SIZE_BYTES)
    finally:
        bz2file.close()
    if verbose:
        util.log_info('... extracted to %s' % targetname)
    return None


def create_bzip2 (archive, compression, cmd, *args, **kwargs):
    """Create a BZIP2 archive with the bz2 Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('creating %s...' % archive)
    if len(args) > 1:
        util.log_error('multi-file compression not supported in Python bz2')
    bz2file = bz2.BZ2File(archive, 'wb')
    try:
        filename = args[0]
        with open(filename, 'rb') as srcfile:
            data = srcfile.read(READ_SIZE_BYTES)
            while data:
                bz2file.write(data)
                data = srcfile.read(READ_SIZE_BYTES)
            if verbose:
                util.log_info('... added %s' % filename)
    finally:
        bz2file.close()
    return None
