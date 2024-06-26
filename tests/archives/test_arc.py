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
"""Test the arc program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestArc(ArchiveTest):
    """Test class for the arc program"""

    program = 'arc'

    @needs_program(program)
    def test_arc(self):
        """Run archive commands with ARC archive."""
        self.archive_commands(self.filename + '.arc', check=Content.Multifile)

    @needs_program('file')
    @needs_program(program)
    def test_arc_file(self):
        """Run archive commands with renamed ARC archive."""
        self.archive_commands(
            self.filename + '.arc.foo', check=Content.Multifile, skip_create=True
        )


class TestArcPassword(TestArc):
    """Test class for the arc program with password protected archives"""

    password = 'thereisnotry'
    filename = 'p'
