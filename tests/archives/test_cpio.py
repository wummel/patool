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
"""Test the cpio program"""

from . import ArchiveTest
from .. import needs_program
from patoolib import util


class TestCpio(ArchiveTest):
    """Test class for the cpio program"""

    program = 'cpio'

    @needs_program(program)
    def test_cpio(self):
        """Run archive commands with CPIO archive."""
        self.archive_commands('t.cpio')

    @needs_program('file')
    @needs_program(program)
    def test_cpio_file(self):
        """Run archive commands with renamed CPIO archive."""
        self.archive_commands('t.cpio.foo', skip_create=True)

    @needs_program('file')
    @needs_program(program)
    def test_cpio_compressed(self):
        """Run archive commands with compressed CPIO archives."""
        for compression, filename in (
            ('gzip', 't.cpio.gz'),
            ('xz', 't.cpio.xz'),
            ('zstd', 't.cpio.zst'),
        ):
            with self.subTest(compression=compression):
                if not util.find_program(compression):
                    self.skipTest(f"program `{compression}' not available")
                self.archive_commands(filename, skip_create=True)
