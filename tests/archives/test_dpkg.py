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
"""Test the dpkg-deb program"""
from . import ArchiveTest
from .. import needs_program


class TestDpkg(ArchiveTest):
    """Test class for the dpkg-deb program"""

    program = "dpkg-deb"

    @needs_program(program)
    def test_dpkg(self):
        """List, extract and test a DEB archive."""
        self.archive_list("t.deb")
        self.archive_extract("t.deb", check=None)
        self.archive_test("t.deb")

    @needs_program("file")
    @needs_program(program)
    def test_dpkg_file(self):
        """List, extract and test a renamed DEB archive."""
        self.archive_list("t.deb.foo")
        self.archive_extract("t.deb.foo", check=None)
        self.archive_test("t.deb.foo")
