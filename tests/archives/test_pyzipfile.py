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
"""Test the python zipfile module"""

from . import ArchiveTest
from .. import needs_program


class TestPyzipfile(ArchiveTest):
    """Test class for the python zipfile module"""

    program = 'py_zipfile'

    def test_py_zipfile(self):
        """Run archive commands with ZIP and CBZ archive."""
        self.archive_commands(self.filename + '.zip')
        self.archive_commands(self.filename + '.cbz')

    @needs_program('file')
    def test_py_zipfile_file(self):
        """Run archive commands with renamed ZIP and CBZ archive."""
        self.archive_commands(self.filename + '.zip.foo', skip_create=True)
        self.archive_commands(self.filename + '.cbz.foo', skip_create=True)


class TestPyzipPasswordfile(TestPyzipfile):
    """Test class for the python zipfile module with password protection"""

    filename = 'p'
    password = 'thereisnotry'
