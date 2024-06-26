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
"""Test the unadf program"""

from . import ArchiveTest
from .. import needs_program


class TestUnadf(ArchiveTest):
    """Test class for the unadf program"""

    program = 'unadf'

    @needs_program(program)
    def test_unadf(self):
        """Extract, list and test an ADF archive"""
        self.archive_extract('t.adf', check=None)
        self.archive_list('t.adf')
        self.archive_test('t.adf')

    @needs_program('file')
    @needs_program(program)
    def test_unadf_file(self):
        """Extract, list and test a renamed ADF archive"""
        self.archive_extract('t.adf.foo', check=None)
        self.archive_test('t.adf.foo')
        self.archive_list('t.adf.foo')
