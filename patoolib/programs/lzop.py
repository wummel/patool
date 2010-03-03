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
"""Archive commands for the lzop program."""
from .. import util


def extract_lzop (archive, encoding, cmd, **kwargs):
    """Extract a LZOP archive."""
    cmdlist = [cmd]
    cmdlist.extend(['-c', '-d'])
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.append('--')
    outfile = util.get_single_outfile(kwargs['outdir'], archive)
    cmdlist.extend([archive, '>', outfile])
    # note that for shell calls the command must be a string
    cmd = " ".join([util.shell_quote(x) for x in cmdlist])
    return (cmd, {'shell': True})

def list_lzop (archive, encoding, cmd, **kwargs):
    """List a LZOP archive."""
    cmdlist = [cmd]
    cmdlist.append('--list')
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(['--', archive])
    return cmdlist

def test_lzop (archive, encoding, cmd, **kwargs):
    """Test a LZOP archive."""
    cmdlist = [cmd]
    cmdlist.append('--test')
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(['--', archive])
    return cmdlist

def create_lzop (archive, encoding, cmd, *args, **kwargs):
    """Create a LZOP archive."""
    cmdlist = [cmd]
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(['-o', archive])
    cmdlist.append('--')
    cmdlist.extend(args)
    return cmdlist
