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
"""Archive commands for the rar program."""
import os

def extract_rar (archive, encoding, cmd, **kwargs):
    """Extract a RAR archive."""
    cmdlist = [cmd, 'x']
    if not kwargs['verbose']:
        cmdlist.append('-c-')
    cmdlist.extend(['-r', '--', os.path.abspath(archive)])
    return (cmdlist, {'cwd': kwargs['outdir']})

def list_rar (archive, encoding, cmd, **kwargs):
    """List a RAR archive."""
    cmdlist = [cmd]
    if kwargs['verbose']:
        cmdlist.append('v')
    else:
        cmdlist.append('l')
        cmdlist.append('-c-')
    cmdlist.extend(['--', archive])
    return cmdlist

def test_rar (archive, encoding, cmd, **kwargs):
    """Test a RAR archive."""
    cmdlist = [cmd, 't']
    if not kwargs['verbose']:
        cmdlist.append('-c-')
    cmdlist.extend(['--', archive])
    return cmdlist

def create_rar (archive, encoding, cmd, *args, **kwargs):
    """Create a RAR archive."""
    cmdlist = [cmd, 'a']
    if not kwargs['verbose']:
        cmdlist.append('-c-')
    cmdlist.extend(['-r', '--', archive])
    cmdlist.extend(args)
    return cmdlist
