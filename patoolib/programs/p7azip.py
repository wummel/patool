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
"""Archive commands for the 7za program.

From the man page:
7za is a stand-alone executable. 7za handles less archive formats than 7z,
but does not need any others.
"""

def extract_7z (archive, encoding, cmd, **kwargs):
    """Extract a 7z archive."""
    cmdlist = [cmd, 'x']
    if not kwargs['verbose']:
        cmdlist.append('-bd')
    cmdlist.extend(['-o%s' % kwargs['outdir'], '--', archive])
    return cmdlist

extract_bzip2 = \
  extract_gzip = \
  extract_zip = \
  extract_compress = \
  extract_rar = \
  extract_cab = \
  extract_7z

def list_7z (archive, encoding, cmd, **kwargs):
    """List a 7z archive."""
    cmdlist = [cmd, 'l']
    if not kwargs['verbose']:
        cmdlist.append('-bd')
    cmdlist.append('--')
    cmdlist.append(archive)
    return cmdlist

list_bzip2 = \
  list_gzip = \
  list_zip = \
  list_compress = \
  list_rar = \
  list_cab = \
  list_rpm = \
  list_7z


def test_7z (archive, encoding, cmd, **kwargs):
    """Test a 7z archive."""
    cmdlist = [cmd, 't']
    if not kwargs['verbose']:
        cmdlist.append('-bd')
    cmdlist.append('--')
    cmdlist.append(archive)
    return cmdlist

test_bzip2 = \
  test_gzip = \
  test_zip = \
  test_compress = \
  test_rar = \
  test_cab = \
  test_7z


def create_7z (archive, encoding, cmd, *args, **kwargs):
    """Create a 7z archive."""
    cmdlist = [cmd, 'a']
    if not kwargs['verbose']:
        cmdlist.append('-bd')
    cmdlist.append('--')
    cmdlist.append(archive)
    cmdlist.extend(args)
    return cmdlist
