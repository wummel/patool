# Copyright (C) 2025 Bastian Kleineidam
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
"""Test the FreeArc arc program"""

from . import ArchiveTest, Content
from .. import needs_program, needs_codec


class TestFreeArc(ArchiveTest):
    """Test class for the FreeArc arc program"""

    program = 'arc'

    @needs_program(program)
    @needs_codec(program, 'freearc')
    def test_freearc(self):
        """Run archive commands with FREEARC archive."""
        self.archive_commands(
            self.filename + '.freearc.arc', check=Content.Multifile, skip_create=True
        )
