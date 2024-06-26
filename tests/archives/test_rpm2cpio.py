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
"""Test the rpm2cpio program"""

from . import ArchiveTest
from .. import needs_program


class TestRpm2cpio(ArchiveTest):
    """Test class for the rpm2cpio program"""

    program = 'rpm2cpio'

    @needs_program(program)
    @needs_program('cpio')
    def test_rpm2cpio(self):
        """Extract an RPM archive."""
        self.archive_extract('t.rpm', check=None)

    @needs_program('file')
    @needs_program(program)
    @needs_program('cpio')
    def test_rpm2cpio_file(self):
        """Extract a renamed RPM archive."""
        self.archive_extract('t.rpm.foo', check=None)
