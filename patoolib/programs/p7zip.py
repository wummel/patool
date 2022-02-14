# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Bastian Kleineidam
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
"""Archive commands for the 7z program."""

def _maybe_add_password(cmdlist, password):
    if password:
        cmdlist.append('-p%s' % password)

def _maybe_disable_interactivity(cmdlist, interactive, password):
    if not interactive:
        cmdlist.append('-y')
        if not password:
            cmdlist.append('-p-')

def extract_7z(archive, compression, cmd, verbosity, interactive, outdir, password=None):
    """Extract a 7z archive."""
    cmdlist = [cmd, 'x']
    _maybe_disable_interactivity(cmdlist, interactive, password)
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-o%s' % outdir, '--', archive])
    return cmdlist

def extract_7z_singlefile(archive, compression, cmd, verbosity, interactive, outdir, password=None):
    """Extract a singlefile archive (eg. gzip or bzip2) with '7z e'.
    This makes sure a single file and no subdirectories are created,
    which would cause errors with patool repack."""
    cmdlist = [cmd, 'e']
    _maybe_disable_interactivity(cmdlist, interactive, password)
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-o%s' % outdir, '--', archive])
    return cmdlist

extract_bzip2 = \
  extract_gzip = \
  extract_compress = \
  extract_xz = \
  extract_lzma = \
  extract_7z_singlefile

extract_zip = \
  extract_rar = \
  extract_cab = \
  extract_arj = \
  extract_cpio = \
  extract_rpm = \
  extract_deb = \
  extract_iso = \
  extract_vhd = \
  extract_7z

def list_7z (archive, compression, cmd, verbosity, interactive, password=None):
    """List a 7z archive."""
    cmdlist = [cmd, 'l']
    _maybe_disable_interactivity(cmdlist, interactive, password)
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['--', archive])
    return cmdlist

list_bzip2 = \
  list_gzip = \
  list_zip = \
  list_compress = \
  list_rar = \
  list_cab = \
  list_arj = \
  list_cpio = \
  list_rpm = \
  list_deb = \
  list_iso = \
  list_xz = \
  list_lzma = \
  list_vhd = \
  list_7z


def test_7z (archive, compression, cmd, verbosity, interactive, password=None):
    """Test a 7z archive."""
    cmdlist = [cmd, 't']
    _maybe_disable_interactivity(cmdlist, interactive, password)
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['--', archive])
    return cmdlist

test_bzip2 = \
  test_gzip = \
  test_zip = \
  test_compress = \
  test_rar = \
  test_cab = \
  test_arj = \
  test_cpio = \
  test_rpm = \
  test_deb = \
  test_iso = \
  test_xz = \
  test_lzma = \
  test_vhd = \
  test_7z


def create_7z(archive, compression, cmd, verbosity, interactive, filenames, password=None):
    """Create a 7z archive."""
    cmdlist = [cmd, 'a']
    if not interactive:
        cmdlist.append('-y')
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-t7z', '-mx=9', '--', archive])
    cmdlist.extend(filenames)
    return cmdlist


def create_zip(archive, compression, cmd, verbosity, interactive, filenames, password=None):
    """Create a ZIP archive."""
    cmdlist = [cmd, 'a']
    if not interactive:
        cmdlist.append('-y')
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-tzip', '-mx=9', '--', archive])
    cmdlist.extend(filenames)
    return cmdlist


def create_xz(archive, compression, cmd, verbosity, interactive, filenames, password=None):
    """Create an XZ archive."""
    cmdlist = [cmd, 'a']
    if not interactive:
        cmdlist.append('-y')
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-txz', '-mx=9', '--', archive])
    cmdlist.extend(filenames)
    return cmdlist


def create_gzip(archive, compression, cmd, verbosity, interactive, filenames, password=None):
    """Create a GZIP archive."""
    cmdlist = [cmd, 'a']
    if not interactive:
        cmdlist.append('-y')
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-tgzip', '-mx=9', '--', archive])
    cmdlist.extend(filenames)
    return cmdlist


def create_bzip2(archive, compression, cmd, verbosity, interactive, filenames, password=None):
    """Create a BZIP2 archive."""
    cmdlist = [cmd, 'a']
    if not interactive:
        cmdlist.append('-y')
    _maybe_add_password(cmdlist, password)
    cmdlist.extend(['-tbzip2', '-mx=9', '--', archive])
    cmdlist.extend(filenames)
    return cmdlist
