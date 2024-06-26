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
"""Test the 7zr program"""

from . import ArchiveTest
from .. import needs_program


class Test7zr(ArchiveTest):
    """Test class for the 7zr program"""

    program = '7zr'

    @needs_program(program)
    def test_7zr(self):
        """Run archive commands with 7Z archives."""
        self.archive_commands('t .7z')
        self.archive_commands('t .cb7')

    @needs_program('file')
    @needs_program(program)
    def test_7z_file(self):
        """Run archive commands with renamed 7Z archives."""
        self.archive_commands('t.7z.foo', skip_create=True)
        self.archive_commands('t.cb7.foo', skip_create=True)
