# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Bastian Kleineidam
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

class TestPyecho (ArchiveTest):

    program = 'py_echo'

    def test_py_echo (self):
        self.archive_list('t.txt.bz2')
        self.archive_list('t.txt.Z')
        self.archive_list('t.txt.lzma')
        self.archive_list('t.txt.lz')
        self.archive_list('t.txt.lrz')
        self.archive_list('t.txt.rz')
        self.archive_list('t.ape')
        self.archive_list('t.shn')
        self.archive_list('t.flac')

    @needs_program('file')
    def test_py_echo_file (self):
        self.archive_list('t.txt.bz2.foo')
        self.archive_list('t.txt.Z.foo')
        # file(1) does not recognize .lzma files
        #self.archive_list('t.lzma.foo')
        self.archive_list('t.txt.lz.foo')
        self.archive_list('t.txt.lrz')
        self.archive_list('t.txt.rz.foo')
        self.archive_list('t.ape.foo')
        # file(1) does not recognize .shn files
        #self.archive_list('t.shn.foo')
        self.archive_list('t.flac.foo')

