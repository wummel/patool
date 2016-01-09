# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016 Bastian Kleineidam
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
from .. import needs_program

class TestRar (ArchiveTest):

    program = 'rar'

    @needs_program(program)
    def test_rar(self):
        self.archive_commands('t.rar')
        self.archive_commands('t.cbr')

    @needs_program('file')
    @needs_program(program)
    def test_rar_file(self):
        self.archive_commands('t.rar.foo', skip_create=True)
        self.archive_commands('t.cbr.foo', skip_create=True)

