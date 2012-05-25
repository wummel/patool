# -*- coding: utf-8 -*-
# Copyright (C) 2012 Bastian Kleineidam
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
"""Archive commands for the flac program."""
from .. import util

def extract_flac (archive, compression, cmd, **kwargs):
    """Decompress a FLAC archive to a WAV file."""
    outfile = util.get_single_outfile(kwargs['outdir'], archive,
      extension=".wav")
    cmdlist = [cmd, '--decode', archive, '--output-name', outfile]
    return cmdlist


def create_flac (archive, compression, cmd, *args, **kwargs):
    """Compress a WAV file to a FLAC archive."""
    cmdlist = [cmd, args[0], '--output-name', archive]
    return cmdlist


def test_flac (archive, compression, cmd, **kwargs):
    """Test a FLAC file."""
    cmdlist = [cmd, '--test']
    if not kwargs['verbose']:
        cmdlist.append('-s')
    cmdlist.append(archive)
    return cmdlist
