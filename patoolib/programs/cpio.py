# Copyright (C) 2010-2023 Bastian Kleineidam
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
"""Archive commands for the cpio program."""

import os
import sys
from .. import util


def extract_cpio(archive, compression, cmd, verbosity, interactive, outdir):
    """Extract a CPIO archive."""
    cmdlist = [
        util.shell_quote(cmd),
        '--extract',
        '--make-directories',
        '--preserve-modification-time',
    ]
    if sys.platform.startswith('linux') and not cmd.endswith('bsdcpio'):
        cmdlist.extend(
            ['--no-absolute-filenames', '--force-local', '--nonmatching', r'"*\.\.*"']
        )
    if verbosity > 1:
        cmdlist.append('-v')
    if compression:
        cmdlist[0:0] = get_decompress_pipe(archive, compression)
    else:
        cmdlist.extend(['<', util.shell_quote(os.path.abspath(archive))])
    return (cmdlist, {'cwd': outdir, 'shell': True})


def list_cpio(archive, compression, cmd, verbosity, interactive):
    """List a CPIO archive."""
    if compression:
        cmdlist = get_decompress_pipe(archive, compression)
        cmdlist.extend([util.shell_quote(cmd), '-i', '-t'])
        if verbosity > 1:
            cmdlist.append('-v')
        return (cmdlist, {'shell': True})
    cmdlist = [cmd, '-i', '-t']
    if verbosity > 1:
        cmdlist.append('-v')
    cmdlist.extend(['-F', archive])
    return cmdlist


test_cpio = list_cpio


def get_decompress_pipe(archive, compression):
    """Get a shell command list that pipes the decompressed archive into the
    next command, since cpio cannot read compressed archives itself.
    """
    decompressor = util.find_program(compression)
    if not decompressor:
        raise util.PatoolError(f"could not find program {compression}")
    archive = util.shell_quote(os.path.abspath(archive))
    return [util.shell_quote(decompressor), '-c', '-d', archive, '|']


def create_cpio(archive, compression, cmd, verbosity, interactive, filenames):
    """Create a CPIO archive."""
    cmdlist = [util.shell_quote(cmd), '--create']
    if verbosity > 1:
        cmdlist.append('-v')
    if len(filenames) != 0:
        findcmd = ['find']
        findcmd.extend([util.shell_quote(x) for x in filenames])
        findcmd.extend(['-print0', '|'])
        cmdlist[0:0] = findcmd
        cmdlist.append('-0')
    cmdlist.extend([">", util.shell_quote(archive)])
    return (cmdlist, {'shell': True})
