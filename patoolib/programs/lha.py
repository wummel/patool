# -*- coding: utf-8 -*-
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
"""Archive commands for the lha program."""

def extract_lzh (archive, encoding, cmd, **kwargs):
    """Extract a LZH archive."""
    cmdlist = [cmd]
    opts = 'x'
    if kwargs['verbose']:
        opts += 'v'
    opts += "w=%s" % kwargs['outdir']
    cmdlist.extend([opts, archive])
    return cmdlist

def list_lzh (archive, encoding, cmd, **kwargs):
    """List a LZH archive."""
    cmdlist = [cmd]
    if kwargs['verbose']:
        cmdlist.append('v')
    else:
        cmdlist.append('l')
    cmdlist.append(archive)
    return cmdlist

def test_lzh (archive, encoding, cmd, **kwargs):
    """Test a LZH archive."""
    cmdlist = [cmd]
    opts = 't'
    if kwargs['verbose']:
        opts += 'v'
    cmdlist.extend([opts, archive])
    return cmdlist

def create_lzh (archive, encoding, cmd, *args, **kwargs):
    """Create a LZH archive."""
    cmdlist = [cmd]
    opts = 'a'
    if kwargs['verbose']:
        opts += 'v'
    cmdlist.extend([opts, archive])
    cmdlist.extend(args)
    return cmdlist

