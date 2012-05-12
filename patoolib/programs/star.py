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

def extract_tar (archive, compression, cmd, **kwargs):
    """Extract a TAR archive."""
    cmdlist = [cmd, '-x']
    add_star_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.extend(['-C', kwargs['outdir'], 'file=%s' % archive])
    return cmdlist

def list_tar (archive, compression, cmd, **kwargs):
    """List a TAR archive."""
    cmdlist = [cmd, '-n']
    add_star_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.append("file=%s" % archive)
    return cmdlist

test_tar = list_tar

def create_tar (archive, compression, cmd, *args, **kwargs):
    """Create a TAR archive."""
    cmdlist = [cmd, '-c']
    add_star_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.append("file=%s" % archive)
    cmdlist.extend(args)
    return cmdlist

def add_star_opts (cmdlist, compression, verbose):
    """Add default options for the star program."""
    # Note that star autodetects compression compression, but displays a warning
    # which we want to avoid.
    if compression == 'gzip':
        cmdlist.append('-z')
    elif compression == 'compress':
        cmdlist.append('-Z')
    elif compression == 'bzip2':
        cmdlist.append('-bz')
    elif compression in ('lzma', 'xz', 'lzip'):
        # use compress-program option
        cmdlist.append('compress-program=%s' % compression)
    if verbose:
        cmdlist.append('-v')
