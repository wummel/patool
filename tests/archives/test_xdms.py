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
"""Test the xdms program"""

from . import ArchiveTest
from .. import needs_program


class TestXdms(ArchiveTest):
    """Test class for the xdms program"""

    program = 'xdms'

    @needs_program(program)
    def test_xdms(self):
        """Test, extract and list a DMS archive."""
        self.archive_extract('t.dms', check=None)
        self.archive_list('t.dms')
        self.archive_test('t.dms')

    # xdms(1) cannot handle files without '.dms' extension
    # @needs_program(program)
    # def test_xdms_file(self):
    #    """Test, extract and list a renamed DMS archive."""
    #    self.archive_extract('t.dms.foo')
    #    self.archive_test('t.dms.foo')
    #    self.archive_list('t.dms.foo')
