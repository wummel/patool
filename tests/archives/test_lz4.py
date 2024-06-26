# Copyright (C) 2023 Bastian Kleineidam
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
"""Test the lz4 program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestLz4(ArchiveTest):
    """Test class for the lz4 program"""

    program = 'lz4'

    @needs_program(program)
    def test_lz4(self):
        """Run archive commands with LZ4 archive."""
        self.archive_extract('t.txt.lz4', check=Content.Singlefile)
        self.archive_test('t.txt.lz4')
        self.archive_list('t.txt.lz4')
        self.archive_create('t.txt.lz4', check=Content.Singlefile)

    @needs_program('file')
    @needs_program(program)
    def test_lz4_file(self):
        """Run archive commands with renamed LZ4 archive."""
        self.archive_extract('t.txt.lz4.foo', check=Content.Singlefile)
        self.archive_test('t.txt.lz4.foo')
        self.archive_list('t.txt.lz4.foo')
