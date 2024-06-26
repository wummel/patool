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
"""Test the unace program"""

from . import ArchiveTest
from .. import needs_program


class TestUnace(ArchiveTest):
    """Test class for the unace program"""

    program = 'unace'

    @needs_program(program)
    def test_unace(self):
        """Run archive commands with different ACE archives."""
        self.archive_list(self.filename + '.ace')
        self.archive_test(self.filename + '.ace')
        # self.archive_extract(self.filename + '.ace')
        self.archive_list(self.filename + '.cba')
        self.archive_test(self.filename + '.cba')
        # self.archive_extract(self.filename + '.cba')

    @needs_program('file')
    @needs_program(program)
    def test_unace_file(self):
        """Run archive commands with different renamed ACE archives."""
        self.archive_list(self.filename + '.ace.foo')
        self.archive_test(self.filename + '.ace.foo')
        # self.archive_extract(self.filename + '.ace.foo')
        self.archive_list(self.filename + '.cba.foo')
        self.archive_test(self.filename + '.cba.foo')
        # self.archive_extract(self.filename + '.cba.foo')


# TODO: add p.ace, p.ace.foo, p.cba, p.cba.foo with password to repository
# class TestUnacePassword(TestUnace):
#
#     filename = 'p'
#     password = 'thereisnotry'
