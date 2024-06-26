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
"""Test the bzip3 program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestBzip3(ArchiveTest):
    """Test class for the bzip3 program"""

    program = 'bzip3'

    @needs_program(program)
    def test_bzip3(self):
        """Extract, test and create a BZIP3 archive."""
        self.archive_extract('t.txt.bz3', check=Content.Singlefile)
        self.archive_test('t.txt.bz3')
        self.archive_create('t.txt.bz3', check=Content.Singlefile)

    @needs_program('file')
    @needs_program(program)
    def test_bzip3_file(self):
        """Extract and test a renamed BZIP3 archive."""
        self.archive_extract('t.txt.bz3.foo', check=Content.Singlefile)
        self.archive_test('t.txt.bz3.foo')
