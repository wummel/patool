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
"""Test the lha program"""

from . import ArchiveTest
from .. import needs_program


class TestLha(ArchiveTest):
    """Test class for the lha program"""

    program = 'lha'

    @needs_program(program)
    def _test_lha(self):
        """Run archive commands with LHA archive."""
        self.archive_commands('t.lha')

    @needs_program('file')
    @needs_program(program)
    def test_lha_file(self):
        """Run archive commands with renamed LHA archive."""
        self.archive_commands('t.lha.foo', skip_create=True)
