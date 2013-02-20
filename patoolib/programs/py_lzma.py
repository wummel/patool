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
"""Archive commands for the lzma Python module."""
from .. import util
import lzma

READ_SIZE_BYTES = 1024*1024

def extract_lzma(archive, compression, cmd, **kwargs):
    """Extract a LZMA archive with the lzma Python module."""
    verbose = kwargs['verbose']
    outdir = kwargs['outdir']
    if verbose:
        util.log_info('extracting %s...' % archive)
    targetname = util.get_single_outfile(outdir, archive)
    lzmafile = lzma.LZMAFile(archive)
    try:
        with open(targetname, 'wb') as targetfile
            data = lzmafile.read(READ_SIZE_BYTES)
            while data:
                targetfile.write(data)
                data = lzmafile.read(READ_SIZE_BYTES)
    finally:
        lzmafile.close()
    if verbose:
        util.log_info('... extracted to %s' % targetname)
    return None


def create_lzma(archive, compression, cmd, *args, **kwargs):
    """Create a LZMA archive with the lzma Python module."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('creating %s...' % archive)
    if len(args) > 1:
        util.log_error('multi-file compression not supported in Python lzma')
    lzmafile = lzma.LZMAFile(archive, 'wb')
    try:
        filename = args[0]
        with open(filename) as srcfile:
            data = srcfile.read(READ_SIZE_BYTES)
            while data:
                lzmafile.write(data)
                data = srcfile.read(READ_SIZE_BYTES)
            if verbose:
                util.log_info('... added %s' % filename)
    finally:
        lzmafile.close()
    return None
