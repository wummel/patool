# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Bastian Kleineidam
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
"""Archive commands for the lrzip program."""
import os
from .. import util

def extract_lrzip (archive, compression, cmd, **kwargs):
    """Extract a LRZIP archive."""
    # Since extracted files will be placed in the current directory,
    # the cwd argument has to be the output directory.
    cmdlist = [cmd, '-d']
    if kwargs['verbose']:
        cmdlist.append('-v')
    outfile = util.get_single_outfile(kwargs['outdir'], archive)
    cmdlist.extend(["-o", outfile, os.path.abspath(archive)])
    return (cmdlist, {'cwd': kwargs['outdir']})

def test_lrzip (archive, compression, cmd, **kwargs):
    """Test a LRZIP archive."""
    cmdlist = [cmd, '-t']
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.append(archive)
    return cmdlist

def create_lrzip (archive, compression, cmd, *args, **kwargs):
    """Create a LRZIP archive."""
    cmdlist = [cmd, '-o', archive]
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(args)
    return cmdlist
