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
"""Test the BZIP2 program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestBzip2(ArchiveTest):
    """Test class for the bzip2 program"""

    program = 'bzip2'

    @needs_program(program)
    def test_bzip2(self):
        """Extract, test and create a BZIP2 archive."""
        self.archive_extract('t.txt.bz2', check=Content.Singlefile)
        self.archive_test('t.txt.bz2')
        self.archive_create('t.txt.bz2', check=Content.Singlefile)

    @needs_program('file')
    @needs_program(program)
    def test_bzip2_file(self):
        """Extract and test a renamed BZIP2 archive."""
        self.archive_extract('t.txt.bz2.foo', check=Content.Singlefile)
        self.archive_test('t.txt.bz2.foo')
