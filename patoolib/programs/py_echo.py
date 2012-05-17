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
"""Archive commands echoing data, implemented by the Python print
statement."""
from patoolib import util


def list_bzip2 (archive, compression, cmd, **kwargs):
    """List a BZIP2 archive."""
    return stripext(cmd, archive)

def list_compress (archive, compression, cmd, **kwargs):
    """List a compress archive."""
    return stripext(cmd, archive)

def list_lzma (archive, compression, cmd, **kwargs):
    """List a LZMA archive."""
    return stripext(cmd, archive)

def list_xz (archive, compression, cmd, **kwargs):
    """List a XZ archive."""
    return stripext(cmd, archive)

def list_lzip (archive, compression, cmd, **kwargs):
    """List a LZIP archive."""
    return stripext(cmd, archive)

def list_lrzip (archive, compression, cmd, **kwargs):
    """List a LRZIP archive."""
    return stripext(cmd, archive)

def list_rzip (archive, compression, cmd, **kwargs):
    """List a RZIP archive."""
    return stripext(cmd, archive)

def list_ape (archive, compression, cmd, **kwargs):
    """List an APE archive."""
    return stripext(cmd, archive, extension=".wav")

def list_shn (archive, compression, cmd, **kwargs):
    """List a SHN archive."""
    return stripext(cmd, archive, extension=".wav")

def stripext (cmd, archive, extension=""):
    """Print the name without suffix."""
    print util.stripext(archive)+extension
    return None
