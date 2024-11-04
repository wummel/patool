# Copyright (C) 2024 Bastian Kleineidam
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
"""Test the 7zz program"""

from . import ArchiveTest, Content
from .. import needs_program, needs_codec


class Test7zz(ArchiveTest):
    """Test class for the 7zz program"""

    program = '7zz'

    @needs_program(program)
    def test_7zz(self):
        """Run archive commands with archives that 7zz supports."""
        self.archive_commands('t .7z')
        self.archive_commands('t .cb7')
        self.archive_commands('t.zip')
        self.archive_commands('t.cbz')
        self.archive_commands('t.txt.xz', check=Content.Singlefile)
        self.archive_commands('t.wim')
        self.archive_list('t.txt.gz')
        self.archive_list('t.txt.bz2')
        self.archive_list('t.txt.lzma')
        self.archive_list('t.jar')
        self.archive_list('t.txt.Z')
        self.archive_list('t.cab')
        self.archive_list('t.chm')
        self.archive_list('t.arj')
        self.archive_list('t.cpio')
        self.archive_list('t.rpm')
        self.archive_list('t.deb')
        self.archive_list('t.iso')
        self.archive_list('t.vhd')
        self.archive_extract('t.txt.gz', check=Content.Singlefile)
        self.archive_extract('t.txt.bz2', check=Content.Singlefile)
        self.archive_extract('t.txt.lzma', check=Content.Singlefile)
        self.archive_extract('t.jar', check=None)
        self.archive_extract('t.txt.Z', check=Content.Singlefile)
        self.archive_extract('t.cab')
        self.archive_extract('t.chm', check=None)
        self.archive_extract('t.arj')
        self.archive_extract('t.cpio')
        self.archive_extract('t.rpm', check=None)
        self.archive_extract('t.deb', check=None)
        self.archive_extract('t.iso')
        self.archive_extract('t.vhd', check=None)
        self.archive_test('t.txt.gz')
        self.archive_test('t.txt.bz2')
        self.archive_test('t.txt.lzma')
        self.archive_test('t.jar')
        self.archive_test('t.txt.Z')
        self.archive_test('t.cab')
        self.archive_test('t.chm')
        self.archive_test('t.arj')
        self.archive_test('t.cpio')
        self.archive_test('t.rpm')
        self.archive_test('t.deb')
        self.archive_test('t.iso')
        self.archive_test('t.vhd')
        self.archive_create('t.txt.gz', check=Content.Singlefile)
        self.archive_create('t.txt.bz2', check=Content.Singlefile)

    @needs_codec(program, 'rar')
    def test_7zz_rar(self):
        """Run archive commands with RAR archives."""
        # only succeeds with the rar module for 7zz installed
        self.archive_list('t.rar')
        self.archive_extract('t.rar')
        self.archive_test('t.rar')

    @needs_program('file')
    @needs_program(program)
    def test_7zz_file(self):
        """Run archive commands with renamed archives that 7zz supports."""
        self.archive_commands('t.7z.foo', skip_create=True)
        self.archive_commands('t.cb7.foo', skip_create=True)
        self.archive_commands('t.zip.foo', skip_create=True)
        self.archive_commands('t.cbz.foo', skip_create=True)
        self.archive_commands(
            't.txt.xz.foo', skip_create=True, check=Content.Singlefile
        )
        self.archive_commands('t.wim.foo', skip_create=True)
        self.archive_list('t.txt.gz.foo')
        self.archive_list('t.txt.bz2.foo')
        self.archive_list('t.jar.foo')
        self.archive_list('t.txt.Z.foo')
        self.archive_list('t.cab.foo')
        self.archive_list('t.chm.foo')
        self.archive_list('t.arj.foo')
        self.archive_list('t.cpio.foo')
        self.archive_list('t.rpm.foo')
        self.archive_list('t.deb.foo')
        self.archive_list('t.iso.foo')
        self.archive_extract('t.txt.gz.foo', check=None)
        self.archive_extract('t.txt.bz2.foo', check=Content.Singlefile)
        self.archive_extract('t.jar.foo', check=None)
        self.archive_extract('t.txt.Z.foo', check=Content.Singlefile)
        self.archive_extract('t.cab.foo')
        self.archive_extract('t.chm.foo', check=None)
        self.archive_extract('t.arj.foo')
        self.archive_extract('t.cpio.foo')
        self.archive_extract('t.rpm.foo', check=None)
        self.archive_extract('t.deb.foo', check=None)
        self.archive_extract('t.iso.foo')
        self.archive_test('t.txt.gz.foo')
        self.archive_test('t.txt.bz2.foo')
        self.archive_test('t.jar.foo')
        self.archive_test('t.txt.Z.foo')
        self.archive_test('t.cab.foo')
        self.archive_test('t.chm.foo')
        self.archive_test('t.arj.foo')
        self.archive_test('t.cpio.foo')
        self.archive_test('t.rpm.foo')
        self.archive_test('t.deb.foo')
        self.archive_test('t.iso.foo')

    @needs_program('file')
    @needs_codec(program, 'rar')
    def test_7zz_rar_file(self):
        """Run archive commands with renamed RAR archives."""
        # only succeeds with the rar module for 7zz installed
        self.archive_list(self.filename + '.rar.foo')
        self.archive_extract(self.filename + '.rar.foo')
        self.archive_test(self.filename + '.rar.foo')


class Test7zzPassword(ArchiveTest):
    """Test class for the 7zz program with password protected archives"""

    program = '7zz'
    password = 'thereisnotry'

    @needs_program(program)
    def test_7zz(self):
        """Run archive commands with password protected archives for 7zz."""
        self.archive_commands('p .7z')
        self.archive_commands('p.zip')
        self.archive_commands('p.cbz')

    @needs_codec(program, 'rar')
    def test_7zz_rar(self):
        """Run archive commands with password protected RAR archives."""
        # only succeeds with the rar module for 7zz installed
        self.archive_list('p.rar')
        self.archive_extract('p.rar')
        self.archive_test('p.rar')

    @needs_program('file')
    @needs_program(program)
    def test_7zz_file(self):
        """Run archive commands with renamed password protected archives for 7zz."""
        self.archive_commands('p.7z.foo', skip_create=True)
        self.archive_commands('p.zip.foo', skip_create=True)
        self.archive_commands('p.cbz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'rar')
    def test_7zz_rar_file(self):
        """Run archive commands with renamed password protected RAR archives."""
        # only succeeds with the rar module for 7zz installed
        self.archive_list('p.rar.foo')
        self.archive_extract('p.rar.foo')
        self.archive_test('p.rar.foo')
