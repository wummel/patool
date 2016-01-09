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
from .. import needs_program, needs_codec

class TestTar (ArchiveTest):

    program = 'tar'

    @needs_program(program)
    def test_tar (self):
        self.archive_commands('t.tar')
        self.archive_commands('t.cbt')

    @needs_codec(program, 'gzip')
    def test_tar_gz (self):
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    @needs_program(program)
    @needs_program('compress')
    def test_tar_z (self):
        self.archive_commands('t.tar.Z')
        self.archive_commands('t.taz')

    @needs_codec(program, 'bzip2')
    def test_tar_bz2 (self):
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_codec(program, 'lzma')
    def test_tar_lzma (self):
        self.archive_commands('t.tar.lzma')

    # even though clzip would support extracting .lz files, the
    # file(1) --uncompress command does not use it for achive detection
    @needs_program(program)
    @needs_program('lzip')
    def test_tar_lzip (self):
        self.archive_commands('t.tar.lz')

    @needs_codec(program, 'xz')
    def test_tar_xz (self):
        self.archive_commands('t.tar.xz')

    @needs_program('file')
    @needs_program(program)
    def test_tar_file (self):
        self.archive_commands('t.tar.foo', skip_create=True)
        self.archive_commands('t.cbt.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'gzip')
    def test_tar_gz_file (self):
        self.archive_commands('t.tar.gz.foo', skip_create=True)
        self.archive_commands('t.tgz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'compress')
    def test_tar_z_file (self):
        self.archive_commands('t.tar.Z.foo', skip_create=True)
        self.archive_commands('t.taz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'bzip2')
    def test_tar_bz2_file (self):
        self.archive_commands('t.tar.bz2.foo', skip_create=True)
        self.archive_commands('t.tbz2.foo', skip_create=True)

    # file(1) does not recognize .lzma files (at least not with --uncompress)
    #@needs_program('file')
    #@needs_codec(program, 'lzma')
    #def test_tar_lzma_file (self):
    #    self.archive_commands('t.tar.lzma.foo', format="tar", compression="lzma")

    # even though clzip would support extracting .lz files, the
    # file(1) --uncompress command does not use it for achive detection
    @needs_program('lzip')
    @needs_program('file')
    @needs_codec(program, 'lzip')
    def test_tar_lzip_file (self):
        self.archive_commands('t.tar.lz.foo', skip_create=True)

    @needs_program('file')
    @needs_codec(program, 'xz')
    def test_tar_xz_file (self):
        self.archive_commands('t.tar.xz.foo', skip_create=True)
