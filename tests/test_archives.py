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
from tests import ArchiveTest, needs_os, needs_program, needs_codec

class TestArchives (ArchiveTest):

    @needs_program('tar')
    def test_tar (self):
        self.program = 'tar'
        self.archive_commands('t.tar')

    @needs_codec('tar', 'gzip')
    def test_tar_gz (self):
        self.program = 'tar'
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    @needs_program('tar')
    @needs_program('compress')
    def test_tar_z (self):
        self.program = 'tar'
        self.archive_commands('t.tar.Z')
        self.archive_commands('t.taz')

    @needs_codec('tar', 'bzip2')
    def test_tar_bz2 (self):
        self.program = 'tar'
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_codec('tar', 'lzma')
    def test_tar_lzma (self):
        self.program = 'tar'
        self.archive_commands('t.tar.lzma')

    # even though clzip would support extracting .lz files, the
    # file(1) --uncompress command does not use it for achive detection
    @needs_program('tar')
    @needs_program('lzip')
    def test_tar_lzip (self):
        self.program = 'tar'
        self.archive_commands('t.tar.lz')

    @needs_codec('tar', 'xz')
    def test_tar_xz (self):
        self.program = 'tar'
        self.archive_commands('t.tar.xz')

    @needs_program('star')
    def test_star (self):
        self.program = 'star'
        self.archive_commands('t.tar')

    @needs_codec('star', 'gzip')
    def test_star_gz (self):
        self.program = 'star'
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    @needs_program('star')
    @needs_program('compress')
    def test_star_z (self):
        self.program = 'star'
        self.archive_commands('t.tar.Z')
        self.archive_commands('t.taz')

    @needs_codec('star', 'bzip2')
    def test_star_bz2 (self):
        self.program = 'star'
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_codec('star', 'lzma')
    def test_star_lzma (self):
        self.program = 'star'
        self.archive_commands('t.tar.lzma')

    @needs_program('star')
    @needs_program('lzip')
    def test_star_lzip (self):
        self.program = 'star'
        self.archive_commands('t.tar.lz')

    @needs_codec('star', 'xz')
    def test_star_xz (self):
        self.program = 'star'
        self.archive_commands('t.tar.xz')

    def test_py_tarfile (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar')

    def test_py_tarfile_gz (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar.gz')
        self.archive_commands('t.tgz')

    def test_py_tarfile_bz2 (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar.bz2')
        self.archive_commands('t.tbz2')

    @needs_program('bzip2')
    def test_bzip2 (self):
        self.program = 'bzip2'
        self.archive_extract('t .bz2')
        self.archive_test('t .bz2')
        self.archive_create('t .bz2', singlefile=True)

    @needs_program('bzip2')
    def test_py_bz2 (self):
        self.program = 'py_bz2'
        self.archive_extract('t .bz2')
        # bzip2 is used to test the created archive
        self.archive_create('t .bz2', singlefile=True)

    @needs_program('pbzip2')
    def test_pbzip2 (self):
        self.program = 'pbzip2'
        self.archive_extract('t .bz2')
        self.archive_test('t .bz2')
        self.archive_create('t .bz2', singlefile=True)

    @needs_program('lbzip2')
    def test_lbzip2 (self):
        self.program = 'lbzip2'
        self.archive_extract('t .bz2')
        self.archive_test('t .bz2')
        self.archive_create('t .bz2', singlefile=True)

    def test_py_echo (self):
        self.program = 'py_echo'
        self.archive_list('t .bz2')
        self.archive_list('t.Z')
        self.archive_list('t.lzma')
        self.archive_list('t.txt.lz')
        self.archive_list('t.txt.lrz')
        self.archive_list('t.txt.rz')
        self.archive_list('t.ape')

    @needs_program('unzip')
    def test_unzip (self):
        self.program = 'unzip'
        self.archive_extract('t.zip')
        self.archive_list('t.zip')
        self.archive_test('t.zip')
        self.archive_extract('t.jar')
        self.archive_list('t.jar')
        self.archive_test('t.jar')

    @needs_program('zip')
    def test_zip (self):
        self.program = 'zip'
        self.archive_create('t.zip')

    def test_py_zipfile (self):
        self.program = 'py_zipfile'
        self.archive_commands('t.zip')

    @needs_program('gzip')
    def test_gzip (self):
        self.program = 'gzip'
        self.archive_commands('t.gz', singlefile=True)
        self.archive_commands('t.txt.gz', singlefile=True)
        self.archive_extract('t.Z')

    @needs_program('gzip')
    def test_py_gzip (self):
        self.program = 'py_gzip'
        self.archive_extract('t.gz')
        self.archive_extract('t.txt.gz')
        # gzip is used to test the created archive
        self.archive_create('t.gz', singlefile=True)

    @needs_program('pigz')
    def test_pigz (self):
        self.program = 'pigz'
        self.archive_commands('t.gz', singlefile=True)
        self.archive_commands('t.txt.gz', singlefile=True)

    @needs_program('uncompress.real')
    def test_uncompress (self):
        self.program = 'uncompress.real'
        self.archive_extract('t.Z')

    @needs_program('compress')
    def test_compress (self):
        self.program = 'compress'
        self.archive_create('t.Z', singlefile=True)

    @needs_program('7z')
    def test_p7zip (self):
        self.program = '7z'
        self.archive_commands('t .7z')
        self.archive_commands('t.zip')
        self.archive_list('t.gz')
        self.archive_list('t .bz2')
        self.archive_list('t.jar')
        self.archive_list('t.Z')
        self.archive_list('t.cab')
        self.archive_list('t.arj')
        self.archive_list('t.cpio')
        self.archive_list('t.rpm')
        self.archive_list('t.deb')
        self.archive_extract('t.gz')
        self.archive_extract('t .bz2')
        self.archive_extract('t.jar')
        self.archive_extract('t.Z')
        self.archive_extract('t.cab')
        self.archive_extract('t.arj')
        self.archive_extract('t.cpio')
        self.archive_extract('t.rpm')
        self.archive_extract('t.deb')
        self.archive_test('t.gz')
        self.archive_test('t .bz2')
        self.archive_test('t.jar')
        self.archive_test('t.Z')
        self.archive_test('t.cab')
        self.archive_test('t.arj')
        self.archive_test('t.cpio')
        self.archive_test('t.rpm')
        self.archive_test('t.deb')

    @needs_codec('7z', 'rar')
    def test_p7zip_rar (self):
        # only succeeds with the rar module for 7z installed
        self.program = '7z'
        self.archive_list('t.rar')
        self.archive_extract('t.rar')
        self.archive_test('t.rar')

    @needs_program('7za')
    def test_p7azip (self):
        # unsupported actions of the 7za standalone program are commented out
        self.program = '7za'
        self.archive_commands('t .7z')
        self.archive_commands('t.zip')
        self.archive_list('t.gz')
        self.archive_list('t .bz2')
        self.archive_list('t.jar')
        self.archive_list('t.Z')
        self.archive_list('t.cab')
        #self.archive_list('t.arj')
        #self.archive_list('t.cpio')
        self.archive_list('t.rpm')
        #self.archive_list('t.deb')
        self.archive_extract('t.gz')
        self.archive_extract('t .bz2')
        self.archive_extract('t.jar')
        self.archive_extract('t.Z')
        self.archive_extract('t.cab')
        #self.archive_extract('t.arj')
        #self.archive_extract('t.cpio')
        #self.archive_extract('t.rpm')
        #self.archive_extract('t.deb')
        self.archive_test('t.gz')
        self.archive_test('t .bz2')
        self.archive_test('t.jar')
        self.archive_test('t.Z')
        self.archive_test('t.cab')
        #self.archive_test('t.arj')
        #self.archive_test('t.cpio')
        #self.archive_test('t.rpm')
        #self.archive_test('t.deb')

    @needs_program('unrar')
    def test_unrar (self):
        self.program = 'unrar'
        self.archive_list('t.rar')
        self.archive_extract('t.rar')

    @needs_program('rar')
    def test_rar (self):
        self.program = 'rar'
        self.archive_commands('t.rar')

    @needs_program('cabextract')
    def test_cabextract (self):
        self.program = 'cabextract'
        self.archive_list('t.cab')
        self.archive_extract('t.cab')

    @needs_program('orange')
    def test_orange (self):
        self.program = 'orange'
        self.archive_extract('t.cab')

    @needs_program('arj')
    def test_arj (self):
        self.program = 'arj'
        self.archive_commands('t.arj')

    @needs_os('posix')
    @needs_program('ar')
    def test_ar (self):
        self.program = 'ar'
        self.archive_commands('t.a', singlefile=True)

    @needs_program('cpio')
    def test_cpio (self):
        self.program = 'cpio'
        self.archive_list('t.cpio')
        self.archive_extract('t.cpio')
        self.archive_create('t.cpio')

    @needs_program('unace')
    def test_unace (self):
        self.program = 'unace'
        self.archive_list('t.ace')
        self.archive_test('t.ace')
        self.archive_extract('t.ace')

    @needs_program('rpm')
    def test_rpm (self):
        self.program = 'rpm'
        self.archive_list('t.rpm')
        # The rpm test fails on non-rpm system with missing dependencies.
        # I am too lazy to build a tiny rpm with one file
        # and no dependency.
        #self.archive_test('t.rpm')

    @needs_program('rpm2cpio')
    @needs_program('cpio')
    def test_rpm_extract (self):
        self.program = 'rpm2cpio'
        self.archive_extract('t.rpm')

    @needs_program('dpkg-deb')
    def test_dpkg (self):
        self.program = 'dpkg'
        self.archive_list('t.deb')
        self.archive_extract('t.deb')
        self.archive_test('t.deb')

    @needs_program('lzop')
    def test_lzop (self):
        self.program = 'lzop'
        self.archive_commands('t.lzo', singlefile=True)

    @needs_program('lzma')
    def test_lzma (self):
        self.program = 'lzma'
        self.archive_test('t.lzma')
        self.archive_extract('t.lzma')
        self.archive_create('t.lzma', singlefile=True)

    @needs_program('lzip')
    def test_lzip (self):
        self.program = 'lzip'
        self.archive_test('t.txt.lz')
        self.archive_extract('t.txt.lz')
        self.archive_create('t.txt.lz', singlefile=True)

    @needs_program('clzip')
    def test_clzip (self):
        self.program = 'clzip'
        self.archive_test('t.txt.lz')
        self.archive_extract('t.txt.lz')
        self.archive_create('t.txt.lz', singlefile=True)

    @needs_program('plzip')
    def test_plzip (self):
        self.program = 'plzip'
        self.archive_test('t.txt.lz')
        self.archive_extract('t.txt.lz')
        self.archive_create('t.txt.lz', singlefile=True)

    @needs_program('pdlzip')
    def test_pdlzip (self):
        self.program = 'pdlzip'
        self.archive_test('t.txt.lz')
        self.archive_extract('t.txt.lz')
        self.archive_create('t.txt.lz', singlefile=True)

    @needs_program('unalz')
    def test_unalz (self):
        self.program = 'unalz'
        self.archive_test('t.alz')
        self.archive_list('t.alz')
        self.archive_extract('t.alz')

    @needs_program('xz')
    def test_xz (self):
        self.program = 'xz'
        self.archive_commands('t .xz', singlefile=True)

    @needs_program('lha')
    def test_lha (self):
        self.program = 'lha'
        self.archive_commands('t.lha')

    @needs_program('arc')
    def test_arc (self):
        self.program = 'arc'
        self.archive_commands('t.arc', singlefile=True)

    @needs_program('nomarch')
    def test_nomarch (self):
        self.program = 'nomarch'
        self.archive_test('t.arc')
        self.archive_list('t.arc')
        self.archive_extract('t.arc')

    @needs_program('lrzip')
    def test_lrzip (self):
        self.program = 'lrzip'
        self.archive_test('t.txt.lrz')
        self.archive_extract('t.txt.lrz')
        self.archive_create('t.txt.lrz', singlefile=True)

    @needs_program('rzip')
    def test_rzip (self):
        self.program = 'rzip'
        self.archive_extract('t.txt.rz')
        self.archive_create('t.txt.rz', singlefile=True)

    @needs_program('zoo')
    def test_zoo (self):
        self.program = 'zoo'
        # XXX test failure - zoo cannot read its own files back :-(
        #self.archive_commands('t.zoo', singlefile=True)

    @needs_program('xdms')
    def test_xdms (self):
        self.program = 'xdms'
        self.archive_test('t.dms')
        self.archive_extract('t.dms')
        self.archive_list('t.dms')

    @needs_program('mac')
    def test_mac (self):
        self.program = 'mac'
        self.archive_extract('t.ape')
        self.archive_test('t.ape')
        self.archive_create('t.ape', srcfile="t.wav")
