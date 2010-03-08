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
"""Archive commands for the nomarch program."""

def extract_arc (archive, encoding, cmd, **kwargs):
    """Extract a ARC archive."""
    # Since extracted files will be placed in the current directory,
    # the cwd argument has to be the output directory.
    cmdlist = [cmd, archive]
    return (cmdlist, {'cwd': kwargs['outdir']})

def list_arc (archive, encoding, cmd, **kwargs):
    """List a ARC archive."""
    cmdlist = [cmd, '-l']
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.append(archive)
    return cmdlist

def test_arc (archive, encoding, cmd, **kwargs):
    """Test a ARC archive."""
    return [cmd, '-t', archive]
