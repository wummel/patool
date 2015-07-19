# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 Bastian Kleineidam
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
from .. import needs_program, needs_module

class TestPylzma (ArchiveTest):

    program = 'py_lzma'

    @needs_program('xz')
    @needs_module('lzma')
    def test_py_lzma (self):
        self.archive_extract('t.txt.lzma', check=Content.Singlefile)
        self.archive_extract('t.txt.xz', check=Content.Singlefile)
        # xz is used to test the created archive
        self.archive_create('t.txt.lzma', check=Content.Singlefile)
        self.archive_create('t.txt.xz', check=Content.Singlefile)

    @needs_program('file')
    @needs_module('lzma')
    def test_py_lzma_file (self):
        self.archive_extract('t.txt.lzma.foo', check=Content.Singlefile)
        self.archive_extract('t.txt.xz.foo', check=Content.Singlefile)

