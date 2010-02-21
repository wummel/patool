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
"""Archive commands for the cpio program."""
from . import util

def extract_cpio (archive, encoding, cmd, **kwargs):
    """Extract a CPIO archive."""
    cmdlist = [cmd]
    cmdlist.append('--extract')
    cmdlist.append('--make-directories')
    cmdlist.append('--preserve-modification-time')
    cmdlist.append('--no-absolute-filenames')
    cmdlist.append('--force-local')
    cmdlist.extend(['--nonmatching', '"*\.\.*"'])
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(['<', archive])
    cmd = " ".join([util.shell_quote(x) for x in cmdlist])
    return (cmd, {'cwd': kwargs['outdir'], 'shell': True})


def list_cpio (archive, encoding, cmd, **kwargs):
    """List a CPIO archive."""
    cmdlist = [cmd]
    cmdlist.append('-t')
    if kwargs['verbose']:
        cmdlist.append('-v')
    cmdlist.extend(['-F', archive])
    return cmdlist
