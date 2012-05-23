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
"""Archive commands for the GNU tar program."""

def extract_tar (archive, compression, cmd, **kwargs):
    """Extract a TAR archive."""
    cmdlist = [cmd, '--extract']
    add_tar_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.extend(["--file", archive, '--directory', kwargs['outdir']])
    return cmdlist

def list_tar (archive, compression, cmd, **kwargs):
    """List a TAR archive."""
    cmdlist = [cmd, '--list']
    add_tar_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.extend(["--file", archive])
    return cmdlist

test_tar = list_tar

def create_tar (archive, compression, cmd, *args, **kwargs):
    """Create a TAR archive."""
    cmdlist = [cmd, '--create']
    add_tar_opts(cmdlist, compression, kwargs['verbose'])
    cmdlist.extend(["--file", archive, '--'])
    cmdlist.extend(args)
    return cmdlist

def add_tar_opts (cmdlist, compression, verbose):
    if compression == 'gzip':
        cmdlist.append('-z')
    elif compression == 'compress':
        cmdlist.append('-Z')
    elif compression == 'bzip2':
        cmdlist.append('-j')
    elif compression in ('lzma', 'xz', 'lzip'):
        # use the compression name as program name since
        # tar is picky which programs it can use
        program = compression
        # set compression program
        cmdlist.extend(['--use-compress-program', program])
    if verbose:
        cmdlist.append('--verbose')
