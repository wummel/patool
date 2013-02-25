# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Bastian Kleineidam
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
"""Archive commands for the arj program."""

def extract_arj (archive, compression, cmd, **kwargs):
    """Extract a ARJ archive."""
    return [cmd, 'x', '-r', '-y', archive, kwargs['outdir']]


def list_arj (archive, compression, cmd, **kwargs):
    """List a ARJ archive."""
    cmdlist = [cmd]
    if kwargs['verbosity'] > 1:
        cmdlist.append('v')
    else:
        cmdlist.append('l')
    cmdlist.extend(['-r', '-y', archive])
    return cmdlist


def test_arj (archive, compression, cmd, **kwargs):
    """Test a ARJ archive."""
    return [cmd, 't', '-r', '-y', archive]


def create_arj (archive, compression, cmd, *args, **kwargs):
    """Create a ARJ archive."""
    cmdlist = [cmd, 'a', '-r', '-y', archive]
    cmdlist.extend(args)
    return cmdlist
