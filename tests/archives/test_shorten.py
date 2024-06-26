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
"""Test the shorten program"""

from . import ArchiveTest
from .. import needs_program


class TestShorten(ArchiveTest):
    """Test class for the shorten program"""

    program = 'shorten'

    @needs_program(program)
    def test_shorten(self):
        """Extract and create SHORTEN archives."""
        self.archive_extract('t.shn', check=None)
        self.archive_create('t.shn', srcfiles=("t.wav",))

    # file(1) does not recognize .shn files
    # @needs_program('file')
    # @needs_program(program)
    # def test_shorten_file(self):
    #    """Extract a renamed SHORTEN archive."""
    #    self.archive_extract('t.shn.foo', check=None)
