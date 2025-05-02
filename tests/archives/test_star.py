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
"""Test the star program"""

from . import ArchiveTest
from .. import needs_program, needs_codec


class TestStar(ArchiveTest):
    """Test class for the star program"""

    program = 'star'

    @needs_program(program)
    def test_star(self):
        """Run archive commands with TAR archives."""
        self.archive_commands('t.tar')
        self.archive_commands('t.cbt')

    @needs_codec(program, 'gzip')
    def test_star_gz(self):
        """Run archive commands with TAR GZIP archives."""
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    @needs_program(program)
    @needs_program('compress')
    def test_star_z(self):
        """Run archive commands with TAR COMPRESS archives."""
        self.archive_commands('t.tar.Z')
        self.archive_commands('t.taz')

    @needs_codec(program, 'bzip2')
    def test_star_bz2(self):
        """Run archive commands with TAR BZIP2 archives."""
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_codec(program, 'lzma')
    def test_star_lzma(self):
        """Run archive commands with TAR LZMA archive."""
        self.archive_commands('t.tar.lzma')

    @needs_program(program)
    @needs_program('lzip')
    def test_star_lzip(self):
        """Run archive commands with TAR LZIP archive."""
        self.archive_commands('t.tar.lz')

    @needs_codec(program, 'xz')
    def test_star_xz(self):
        """Run archive commands with TAR XZ archive."""
        self.archive_commands('t.tar.xz')

    @needs_program('file')
    @needs_program(program)
    def test_star_file(self):
        """Run archive commands with renamed TAR archives."""
        self.archive_commands('t.tar.foo', skip_create=True)
        self.archive_commands('t.cbt.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'gzip')
    def test_star_gz_file(self):
        """Run archive commands with renamed TAR GZIP archives."""
        self.archive_commands('t.tar.gz.foo', skip_create=True)
        self.archive_commands('t.tgz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'compress')
    def test_star_z_file(self):
        """Run archive commands with renamed TAR COMPRESS archives."""
        self.archive_commands('t.tar.Z.foo', skip_create=True)
        self.archive_commands('t.taz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'bzip2')
    def test_star_bz2_file(self):
        """Run archive commands with renamed TAR BZIP2 archives."""
        self.archive_commands('t.tar.bz2.foo', skip_create=True)
        self.archive_commands('t.tbz2.foo', skip_create=True)

    # file(1) does not recognize .lzma files
    # @needs_program('file')
    # @needs_codec(program, 'lzma')
    # def test_star_lzma_file(self):
    #    """Run archive commands with renamed TAR LZMA archive."""
    #    self.archive_commands('t.tar.lzma.foo', skip_create=True)

    # file(1) does not recognize .lzip files
    # @needs_program('file')
    # @needs_codec(program, 'lzip')
    # def test_star_lzip_file(self):
    #    """Run archive commands with renamed TAR LZIP archive."""
    #    self.archive_commands('t.tar.lz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'xz')
    def test_star_xz_file(self):
        """Run archive commands with renamed TAR XZ archive."""
        self.archive_commands('t.tar.xz.foo', skip_create=True)
