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

class TestZip (ArchiveTest):

    program = 'zip'

    @needs_program(program)
    def test_zip (self):
        self.archive_create('t.zip')
        self.archive_test('t.zip')
        self.archive_create('t.cbz')
        self.archive_test('t.cbz')
        self.archive_create('t.apk')
        self.archive_test('t.apk')
        self.archive_create('t.jar')
        self.archive_test('t.jar')
        self.archive_create('t.epub')
        self.archive_test('t.epub')

    @needs_program('file')
    @needs_program(program)
    def test_zip_file (self):
        self.archive_test('t.zip.foo')
        self.archive_test('t.cbz.foo')
        self.archive_test('t.apk.foo')
        self.archive_test('t.jar.foo')
        self.archive_test('t.epub.foo')
