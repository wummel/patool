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
"""Archive commands for the star program."""

def extract_tar (archive, encoding, cmd, **kwargs):
    """Extract a TAR archive."""
    cmdlist = [cmd, '-x']
    # Note that star autodetects encoding compression, but displays a warning
    # which we want to avoie.
    if encoding == 'gzip':
        cmdlist.append('-z')
    elif encoding == 'compress':
        cmdlist.append('-Z')
    elif encoding == 'bzip2':
        cmdlist.append('-bz')
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(['-C', kwargs['outdir'], 'file=%s' % archive])
    return cmdlist

def list_tar (archive, encoding, cmd, **kwargs):
    """List a TAR archive."""
    cmdlist = [cmd, '-n']
    if encoding == 'gzip':
        cmdlist.append('-z')
    elif encoding == 'compress':
        cmdlist.append('-Z')
    elif encoding == 'bzip2':
        cmdlist.append('-bz')
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.append("file=%s" % archive)
    return cmdlist

test_tar = list_tar
