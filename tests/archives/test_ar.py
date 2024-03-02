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
"""Test the ar program"""
from . import ArchiveTest, Content
from .. import needs_program, needs_os


class TestAr(ArchiveTest):
    """Test class for the ar program"""

    program = "ar"

    @needs_os("posix")
    @needs_program(program)
    def test_ar(self):
        """Run archive commands with AR archive."""
        self.archive_commands("t.txt.a", check=Content.Singlefile)

    @needs_os("posix")
    @needs_program("file")
    @needs_program(program)
    def test_ar_file(self):
        """Run archive commands with renamed AR archive."""
        self.archive_commands("t.txt.a.foo", skip_create=True, check=None)
