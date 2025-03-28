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
"""Standard archive functions for singlefile archives."""

from collections.abc import Sequence
from .. import fileutil, util


def extract_singlefile_standard(
    archive: str,
    compression: str | None,
    cmd: str,
    verbosity: int,
    interactive: bool,
    outdir: str,
) -> tuple[Sequence[str], dict[str, bool]]:
    """Standard routine to extract a singlefile archive (like gzip)."""
    cmdlist = [util.shell_quote(cmd)]
    if verbosity > 1:
        cmdlist.append('-v')
    outfile = fileutil.get_single_outfile(outdir, archive)
    cmdlist.extend(
        ['-c', '-d', '--', util.shell_quote(archive), '>', util.shell_quote(outfile)]
    )
    return (cmdlist, {'shell': True})


def test_singlefile_standard(
    archive: str, compression: str | None, cmd: str, verbosity: int, interactive: bool
) -> Sequence[str]:
    """Standard routine to test a singlefile archive (like gzip)."""
    cmdlist = [cmd]
    if verbosity > 1:
        cmdlist.append('-v')
    cmdlist.extend(['-t', '--', archive])
    return cmdlist


def create_singlefile_standard(
    archive: str,
    compression: str | None,
    cmd: str,
    verbosity: int,
    interactive: bool,
    filenames: Sequence[str],
) -> tuple[Sequence[str], dict[str, bool]]:
    """Standard routine to create a singlefile archive (like gzip)."""
    cmdlist = [util.shell_quote(cmd)]
    if verbosity > 1:
        cmdlist.append('-v')
    cmdlist.extend(['-c', '--'])
    cmdlist.extend([util.shell_quote(x) for x in filenames])
    cmdlist.extend(['>', util.shell_quote(archive)])
    return (cmdlist, {'shell': True})
