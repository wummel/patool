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
"""Archive commands for the ar program."""

def extract_ar (archive, encoding, cmd, **kwargs):
    """Extract a AR archive."""
    cmdlist = [cmd]
    opts = 'x'
    if kwargs['verbose']:
        opts += 'v'
    cmdlist.extend([opts, archive, kwargs['outdir']])
    return cmdlist

def list_ar (archive, encoding, cmd, **kwargs):
    """List a AR archive."""
    cmdlist = [cmd]
    opts = 't'
    if kwargs['verbose']:
        opts += 'v'
    cmdlist.extend([opts, archive])
    return cmdlist

test_ar = list_ar

def create_ar (archive, encoding, cmd, *args, **kwargs):
    """Create a AR archive."""
    cmdlist = [cmd]
    opts = 'rc'
    if kwargs['verbose']:
        opts += 'v'
    cmdlist.extend([opts, archive])
    cmdlist.extend(args)
    return cmdlist

