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
"""Test the rar program"""

from . import ArchiveTest
from .. import needs_program


class TestRar(ArchiveTest):
    """Test class for the rar program"""

    program = 'rar'

    @needs_program(program)
    def test_rar(self):
        """Run archive commands with RAR and CBR archive."""
        self.archive_commands(self.filename + '.rar')
        self.archive_commands(self.filename + '.cbr')

    @needs_program('file')
    @needs_program(program)
    def test_rar_file(self):
        """Run archive commands with renamed RAR and CBR archive."""
        self.archive_commands(self.filename + '.rar.foo', skip_create=True)
        self.archive_commands(self.filename + '.cbr.foo', skip_create=True)


class TestRarPassword(ArchiveTest):
    """Test class for the rar program with password"""

    filename = 'p'
    password = 'thereisnotry'
    program = 'rar'

    @needs_program(program)
    def test_rar(self):
        """Run archive commands with password protected RAR archive."""
        self.archive_commands(self.filename + '.rar')

    @needs_program('file')
    @needs_program(program)
    def test_rar_file(self):
        """Run archive commands with renamed password protected RAR archive."""
        self.archive_commands(self.filename + '.rar.foo', skip_create=True)
