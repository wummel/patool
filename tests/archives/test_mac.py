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
"""Test the mac program"""
from . import ArchiveTest
from .. import needs_program


class TestMac(ArchiveTest):
    """Test class for the mac program"""

    program = "mac"

    @needs_program(program)
    def test_mac(self):
        """Extract, test and create an APE archive."""
        self.archive_extract("t.ape", check=None)
        self.archive_test("t.ape")
        self.archive_create("t.ape", srcfiles=("t.wav",))

    @needs_program("file")
    @needs_program(program)
    def test_mac_file(self):
        """Extract a renamed APE archive."""
        self.archive_extract("t.ape.foo", check=None)
