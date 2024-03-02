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
"""Test the shar program"""
from . import ArchiveTest, Content
from .. import needs_program


class TestShar(ArchiveTest):
    """Test class for the shar program"""

    program = "shar"

    @needs_program(program)
    @needs_program("unshar")
    def test_shar(self):
        """Create a SHAR archive."""
        self.archive_create("t.shar", check=Content.Singlefile)
