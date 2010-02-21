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
"""Archive commands for the GNU tar program."""

def extract_tar (archive, encoding, cmd, **kwargs):
    """Extract a TAR archive."""
    cmdlist = [cmd, '--extract']
    if encoding:
        cmdlist.append('--%s' % encoding)
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(["--file", archive, '--directory', kwargs['outdir']])
    return cmdlist

def list_tar (archive, encoding, cmd, **kwargs):
    """List a TAR archive."""
    cmdlist = [cmd, '--list']
    if encoding:
        cmdlist.append('--%s' % encoding)
    if kwargs['verbose']:
        cmdlist.append('--verbose')
    cmdlist.extend(["--file", archive])
    return cmdlist

def create_tar (archive, encoding, cmd, **kwargs):
    """Create a TAR archive."""
    print "XXX create", archive, encoding, cmd, kwargs
