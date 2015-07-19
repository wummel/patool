# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Bastian Kleineidam
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
from . import ArchiveTest
from .. import needs_program, skip_on_travis

class TestUnadf (ArchiveTest):

    program = 'unadf'

    # On a Travis CI build the test fails.
    @skip_on_travis()
    @needs_program(program)
    def test_unadf(self):
        self.archive_extract('t.adf', check=None)
        self.archive_list('t.adf')
        self.archive_test('t.adf')

    # On a Travis CI build the test fails.
    @skip_on_travis()
    @needs_program('file')
    @needs_program(program)
    def test_unadf_file(self):
        self.archive_extract('t.adf.foo', check=None)
        self.archive_test('t.adf.foo')
        self.archive_list('t.adf.foo')
