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
"""Archive commands for the gzip Python module."""
from __future__ import absolute_import
# now gzip refers to the Python standard module, not the local one
import gzip
from patoolib import util

READ_SIZE_BYTES = 1024*1024

def extract_gzip (archive, encoding, cmd, **kwargs):
    """Extract a GZIP archive with the gzip Python module functionality."""
    verbose = kwargs['verbose']
    if verbose:
        util.log_info('extracting %s...' % archive)
    targetname = util.get_single_outfile(kwargs['outdir'], archive)
    gzipfile = gzip.GzipFile(archive)
    try:
        targetfile = open(targetname, 'wb')
        try:
            data = gzipfile.read(READ_SIZE_BYTES)
            while data:
                targetfile.write(data)
                data = gzipfile.read(READ_SIZE_BYTES)
        finally:
            targetfile.close()
    finally:
        gzipfile.close()
    if verbose:
        util.log_info('... extracted to %s' % targetname)
    return None
