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
"""Archive commands for the lzop program."""
from . import extract_singlefile_standard


extract_lzop = extract_singlefile_standard


def list_lzop (archive, compression, cmd, **kwargs):
    """List a LZOP archive."""
    cmdlist = [cmd, '--list']
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(['--', archive])
    return cmdlist

def test_lzop (archive, compression, cmd, **kwargs):
    """Test a LZOP archive."""
    cmdlist = [cmd, '--test']
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(['--', archive])
    return cmdlist

def create_lzop (archive, compression, cmd, *args, **kwargs):
    """Create a LZOP archive."""
    cmdlist = [cmd]
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(['-o', archive, '--'])
    cmdlist.extend(args)
    return cmdlist
