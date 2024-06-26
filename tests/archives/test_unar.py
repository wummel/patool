# Copyright (C) 2023-2024 Bastian Kleineidam
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
"""Test the unar program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestUnar(ArchiveTest):
    """Test class for the unar program"""

    program = 'unar'

    @needs_program(program)
    def test_unar(self):
        """Extract different archives."""
        self.archive_extract(self.filename + '.rar')
        self.archive_extract(self.filename + '.zip')
        self.archive_extract(self.filename + ' .7z')
        self.archive_extract(self.filename + '.tar')
        self.archive_extract(self.filename + '.txt.gz', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.bz2', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.lzma', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.xz', check=Content.Singlefile)
        self.archive_extract(self.filename + '.cab')
        self.archive_extract(self.filename + '.iso')
        self.archive_extract(self.filename + '.cpio')
        self.archive_extract(self.filename + '.txt.Z', check=Content.Singlefile)
        self.archive_extract(self.filename + '.zoo', check=Content.Multifile)
        self.archive_extract(self.filename + '.dms', check=None)

    @needs_program('file')
    @needs_program(program)
    def test_unar_file(self):
        """Extract renamed different archives."""
        self.archive_extract(self.filename + '.rar.foo')
        self.archive_extract(self.filename + '.7z.foo')
        self.archive_extract(self.filename + '.tar.foo')
        self.archive_extract(self.filename + '.txt.gz.foo', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.bz2.foo', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.lzma.foo', check=Content.Singlefile)
        self.archive_extract(self.filename + '.txt.xz.foo', check=Content.Singlefile)
        self.archive_extract(self.filename + '.cab.foo')
        self.archive_extract(self.filename + '.iso.foo')
        self.archive_extract(self.filename + '.cpio.foo')
        self.archive_extract(self.filename + '.txt.Z.foo', check=Content.Singlefile)
        self.archive_extract(self.filename + '.zoo.foo', check=Content.Multifile)


class TestUnarPassword(ArchiveTest):
    """Test class for the unar program with password protected archives"""

    program = 'unar'
    password = 'thereisnotry'

    @needs_program(program)
    def test_unar(self):
        """Run archive commands with password protected archives for unar."""
        self.archive_extract('p.zip')
