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
"""Test the zpaq program"""
from . import ArchiveTest, Content
from .. import needs_program


class TestZpaq(ArchiveTest):
    """Test class for the zpaq program"""

    program = "zpaq"

    @needs_program(program)
    def test_zpaq(self):
        """Run archive commands with ZPAQ archive."""
        self.archive_commands("t.zpaq", check=Content.Multifile)

    @needs_program("file")
    @needs_program(program)
    def test_zpaq_file(self):
        """Run archive commands with renamed ZPAQ archive."""
        self.archive_extract("t.zpaq.foo", check=Content.Multifile)
        self.archive_test("t.zpaq.foo")
        self.archive_list("t.zpaq.foo")
