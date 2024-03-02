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
"""Archive commands for the unalz program."""


def _maybe_add_password(cmdlist, password):
    if password:
        cmdlist.extend(["-pwd", password])


def extract_alzip(
    archive, compression, cmd, verbosity, interactive, outdir, password=None
):
    """Extract a ALZIP archive."""
    cmdlist = [cmd, "-d", outdir]
    _maybe_add_password(cmdlist, password)
    cmdlist.append(archive)
    return cmdlist


def list_alzip(archive, compression, cmd, verbosity, interactive, password=None):
    """List a ALZIP archive."""
    cmdlist = [cmd, "-l"]
    _maybe_add_password(cmdlist, password)
    cmdlist.append(archive)
    return cmdlist


test_alzip = list_alzip
