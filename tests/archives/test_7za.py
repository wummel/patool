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
"""Test the 7za program"""

from . import ArchiveTest, Content
from .. import needs_program, needs_codec


class Test7za(ArchiveTest):
    """Test class for the 7za program"""

    program = '7za'

    @needs_program(program)
    def test_7za(self):
        """Run archive commands with archives that 7za supports."""
        self.archive_commands('t .7z')
        self.archive_commands('t .cb7')
        self.archive_commands('t.zip')
        self.archive_commands('t.cbz')
        self.archive_list('t.txt.gz')
        self.archive_list('t.txt.bz2')
        self.archive_list('t.jar')
        self.archive_list('t.cab')
        self.archive_list('t.rpm')
        self.archive_extract('t.txt.gz', check=Content.Singlefile)
        self.archive_extract('t.txt.bz2', check=Content.Singlefile)
        self.archive_extract('t.jar', check=None)
        self.archive_extract('t.cab')
        self.archive_test('t.txt.gz')
        self.archive_test('t.txt.bz2')
        self.archive_test('t.jar')
        self.archive_test('t.cab')
        self.archive_create('t.txt.gz', check=Content.Singlefile)
        self.archive_create('t.txt.bz2', check=Content.Singlefile)

    @needs_program(program)
    @needs_codec(program, 'compress')
    def test_7za_compress(self):
        """Run archive commands with compress archives."""
        self.archive_list('t.txt.Z')
        self.archive_extract('t.txt.Z', check=Content.Singlefile)
        self.archive_test('t.txt.Z')

    @needs_program('file')
    @needs_program(program)
    def test_7za_file(self):
        """Run archive commands with renamed archives that 7za supports."""
        self.archive_commands('t.7z.foo', skip_create=True)
        self.archive_commands('t.cb7.foo', skip_create=True)
        self.archive_commands('t.zip.foo', skip_create=True)
        self.archive_commands('t.cbz.foo', skip_create=True)
        self.archive_list('t.txt.gz.foo')
        self.archive_list('t.txt.bz2.foo')
        self.archive_list('t.jar.foo')
        self.archive_list('t.cab.foo')
        self.archive_list('t.rpm.foo')
        self.archive_extract('t.txt.gz.foo', check=None)
        self.archive_extract('t.txt.bz2.foo', check=Content.Singlefile)
        self.archive_extract('t.jar.foo', check=None)
        self.archive_extract('t.cab.foo')
        self.archive_test('t.txt.gz.foo')
        self.archive_test('t.txt.bz2.foo')
        self.archive_test('t.jar.foo')
        self.archive_test('t.cab.foo')

    @needs_program('file')
    @needs_program(program)
    @needs_codec(program, 'compress')
    def test_7za_compress_file(self):
        """Run archive commands with renamed compress archives."""
        self.archive_list('t.txt.Z.foo')
        self.archive_extract('t.txt.Z.foo', check=Content.Singlefile)
        self.archive_test('t.txt.Z.foo')
