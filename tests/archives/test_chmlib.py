# Copyright (C) 2012-2023 Bastian Kleineidam
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
"""Test the extract_chmLib program"""
from . import ArchiveTest
from .. import needs_program


class TestChmlib(ArchiveTest):
    """Test class for the extract_chmLib program"""

    program = "extract_chmLib"

    @needs_program(program)
    def test_chmlib(self):
        """Extract a CHM archive."""
        self.archive_extract("t.chm", check=None)

    @needs_program("file")
    @needs_program(program)
    def test_chmlib_file(self):
        """Extract a renamed CHM archive."""
        self.archive_extract("t.chm.foo", check=None)
