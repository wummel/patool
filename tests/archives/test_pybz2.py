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
from . import ArchiveTest, Content
from .. import needs_program

class TestPybz2 (ArchiveTest):

    program = 'py_bz2'

    @needs_program('bzip2')
    def test_py_bz2 (self):
        self.archive_extract('t.txt.bz2', check=Content.Singlefile)
        # bzip2 is used to test the created archive
        self.archive_create('t.txt.bz2', check=Content.Singlefile)

    @needs_program('file')
    def test_py_bz2_file (self):
        self.archive_extract('t.txt.bz2.foo', check=Content.Singlefile)

