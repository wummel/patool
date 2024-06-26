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
"""Test the rzip program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestRzip(ArchiveTest):
    """Test class for the rzip program"""

    program = 'rzip'

    @needs_program(program)
    def test_rzip(self):
        """Extract and create an RZIP archive."""
        self.archive_extract('t.txt.rz', check=Content.Singlefile)
        self.archive_create('t.txt.rz', check=Content.Singlefile)

    @needs_program(program)
    def test_rzip_file(self):
        """Extract a renamed RZIP archive."""
        self.archive_extract('t.txt.rz.foo', check=Content.Singlefile)
