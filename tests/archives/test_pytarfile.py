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

class TestPytarfile (ArchiveTest):

    program = 'py_tarfile'

    def test_py_tarfile (self):
        self.archive_commands('t.tar')
        self.archive_commands('t.cbt')

    def test_py_tarfile_gz (self):
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    def test_py_tarfile_bz2 (self):
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_program('file')
    def test_py_tarfile_file (self):
        self.archive_commands('t.tar.foo', skip_create=True)
        self.archive_commands('t.cbt.foo', skip_create=True)

    @needs_program('file')
    def test_py_tarfile_gz_file (self):
        self.archive_commands('t.tar.gz.foo', skip_create=True)
        self.archive_commands('t.tgz.foo', skip_create=True)

    @needs_program('file')
    def test_py_tarfile_bz2_file (self):
        self.archive_commands('t.tar.bz2.foo', skip_create=True)
        self.archive_commands('t.tbz2.foo', skip_create=True)
