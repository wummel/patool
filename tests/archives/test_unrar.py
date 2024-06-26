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
"""Test the unrar program"""

from . import ArchiveTest
from .. import needs_program


class TestUnrar(ArchiveTest):
    """Test class for the unrar program"""

    program = 'unrar'

    @needs_program(program)
    def test_unrar(self):
        """List and extract a RAR archive."""
        self.archive_list('t.rar')
        self.archive_extract('t.rar')

    @needs_program('file')
    @needs_program(program)
    def test_unrar_file(self):
        """List and extract a renamed RAR archive."""
        self.archive_list('t.rar.foo')
        self.archive_extract('t.rar.foo')
