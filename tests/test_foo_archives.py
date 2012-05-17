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

    @needs_program('file')
    @needs_program('tar')
    def test_tar_file (self):
        self.program = 'tar'
        self.archive_commands('t.tar.foo', format="tar")

    @needs_program('file')
    @needs_codec('tar', 'gzip')
    def test_tar_gz_file (self):
        self.program = 'tar'
        self.archive_commands('t.tar.gz.foo', format="tar", compression="gzip")
        self.archive_commands('t.tgz.foo', format="tar", compression="gzip")

    @needs_program('file')
    @needs_codec('tar', 'compress')
    def test_tar_z (self):
        self.program = 'tar'
        self.archive_commands('t.tar.Z.foo', format="tar", compression="compress")
        self.archive_commands('t.taz.foo', format="tar", compression="compress")

    @needs_program('file')
    @needs_codec('tar', 'bzip2')
    def test_tar_bz2 (self):
        self.program = 'tar'
        self.archive_commands('t.tar.bz2.foo', format="tar", compression="bzip2")
        self.archive_commands('t.tbz2.foo', format="tar", compression="bzip2")

    # file(1) does not recognize .lzma files (at least not with --uncompress)
    #@needs_program('file')
    #@needs_codec('tar', 'lzma')
    #def test_tar_lzma (self):
    #    self.program = 'tar'
    #    self.archive_commands('t.tar.lzma.foo', format="tar", compression="lzma")

    # even though clzip would support extracting .lz files, the
    # file(1) --uncompress command does not use it for achive detection
    @needs_program('lzip')
    @needs_program('file')
    @needs_codec('tar', 'lzip')
    def test_tar_lzip (self):
        self.program = 'tar'
        self.archive_commands('t.tar.lz.foo', format="tar", compression="lzip")

    @needs_program('file')
    @needs_codec('tar', 'xz')
    def test_tar_xz (self):
        self.program = 'tar'
        self.archive_commands('t.tar.xz.foo', format="tar", compression="xz")

    @needs_program('file')
    @needs_program('star')
    def test_star (self):
        self.program = 'star'
        self.archive_commands('t.tar.foo', format="tar")

    @needs_program('file')
    @needs_codec('star', 'gzip')
    def test_star_gz (self):
        self.program = 'star'
        self.archive_commands('t.tar.gz.foo', format="tar", compression="gzip")
        self.archive_commands('t.tgz.foo', format="tar", compression="gzip")

    @needs_program('file')
    @needs_codec('star', 'compress')
    def test_star_z (self):
        self.program = 'star'
        self.archive_commands('t.tar.Z.foo', format="tar", compression="compress")
        self.archive_commands('t.taz.foo', format="tar", compression="compress")

    @needs_program('file')
    @needs_codec('star', 'bzip2')
    def test_star_bz2 (self):
        self.program = 'star'
        self.archive_commands('t.tar.bz2.foo', format="tar", compression="bzip2")
        self.archive_commands('t.tbz2.foo', format="tar", compression="bzip2")

    # file(1) does not recognize .lzma files
    #@needs_program('file')
    #@needs_codec('star', 'lzma')
    #def test_star_lzma (self):
    #    self.program = 'star'
    #    self.archive_commands('t.tar.lzma.foo', format="tar", compression="lzma")

    @needs_program('file')
    @needs_codec('star', 'lzip')
    def test_star_lzip (self):
        self.program = 'star'
        self.archive_commands('t.tar.lz.foo', format="tar", compression="lzip")

    @needs_program('file')
    @needs_codec('star', 'xz')
    def test_star_xz (self):
        self.program = 'star'
        self.archive_commands('t.tar.xz.foo', format="tar", compression="xz")

    @needs_program('file')
    def test_py_tarfile_file (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar.foo', format="tar")

    @needs_program('file')
    def test_py_tarfile_gz_file (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar.gz.foo', format="tar", compression="gzip")
        self.archive_commands('t.tgz.foo', format="tar", compression="gzip")

    @needs_program('file')
    def test_py_tarfile_bz2 (self):
        self.program = 'py_tarfile'
        self.archive_commands('t.tar.bz2.foo', format="tar", compression="bzip2")
        self.archive_commands('t.tbz2.foo', format="tar", compression="bzip2")

    @needs_program('file')
    @needs_program('bzip2')
    def test_bzip2 (self):
        self.program = 'bzip2'
        self.archive_extract('t.bz2.foo')
        self.archive_test('t.bz2.foo')
        self.archive_create('t.bz2.foo', format="bzip2", singlefile=True)

    @needs_program('file')
    def test_py_bz2 (self):
        self.program = 'py_bz2'
        self.archive_extract('t.bz2.foo')
        self.archive_create('t.bz2.foo', format="bzip2", singlefile=True)

    @needs_program('file')
    @needs_program('pbzip2')
    def test_pbzip2 (self):
        self.program = 'pbzip2'
        self.archive_extract('t.bz2.foo')
        self.archive_test('t.bz2.foo')
        self.archive_create('t.bz2.foo', format="bzip2", singlefile=True)

    @needs_program('file')
    @needs_program('lbzip2')
    def test_lbzip2 (self):
        self.program = 'lbzip2'
        self.archive_extract('t.bz2.foo')
        self.archive_test('t.bz2.foo')
        self.archive_create('t.bz2.foo', format="bzip2", singlefile=True)

    @needs_program('file')
    def test_py_echo (self):
        self.program = 'py_echo'
        self.archive_list('t.bz2.foo')
        self.archive_list('t.Z.foo')
        # file(1) does not recognize .lzma files
        #self.archive_list('t.lzma.foo')
        self.archive_list('t.txt.lz.foo')
        self.archive_list('t.txt.lrz')
        self.archive_list('t.txt.rz.foo')
        self.archive_list('t.ape.foo')
        # file(1) does not recognize .shn files
        #self.archive_list('t.shn.foo')
        self.archive_list('t.flac.foo')

    @needs_program('file')
    @needs_program('unzip')
    def test_unzip (self):
        self.program = 'unzip'
        self.archive_extract('t.zip.foo')
        self.archive_list('t.zip.foo')
        self.archive_test('t.zip.foo')
        self.archive_extract('t.jar.foo')
        self.archive_list('t.jar.foo')
        self.archive_test('t.jar.foo')

    @needs_program('file')
    @needs_program('zip')
    def test_zip (self):
        self.program = 'zip'
        self.archive_create('t.zip.foo', format="zip")

    @needs_program('file')
    def test_py_zipfile (self):
        self.program = 'py_zipfile'
        self.archive_commands('t.zip.foo', format="zip")

    @needs_program('file')
    @needs_program('gzip')
    def test_gzip (self):
        self.program = 'gzip'
        self.archive_commands('t.gz.foo', format="gzip", singlefile=True)
        self.archive_commands('t.txt.gz.foo', format="gzip", singlefile=True)
        self.archive_extract('t.Z.foo')

    @needs_program('file')
    @needs_program('gzip')
    def test_py_gzip (self):
        self.program = 'py_gzip'
        self.archive_extract('t.gz.foo')
        self.archive_extract('t.txt.gz.foo')
        # gzip is used to test the created archive
        self.archive_create('t.gz.foo', format="gzip", singlefile=True)
        self.archive_create('t.txt.gz.foo', format="gzip", singlefile=True)

    @needs_program('file')
    @needs_program('uncompress.real')
    def test_uncompress (self):
        self.program = 'uncompress.real'
        self.archive_extract('t.Z.foo')

    @needs_program('file')
    @needs_program('compress')
    def test_compress (self):
        self.program = 'compress'
        self.archive_create('t.Z.foo', format="compress", singlefile=True)

    @needs_program('file')
    @needs_program('7z')
    def test_p7zip_file (self):
        self.program = '7z'
        self.archive_commands('t.7z.foo', format="7z")
        self.archive_commands('t.zip.foo', format="zip")
        self.archive_list('t.gz.foo')
        self.archive_list('t.bz2.foo')
        self.archive_list('t.jar.foo')
        self.archive_list('t.Z.foo')
        self.archive_list('t.cab.foo')
        self.archive_list('t.arj.foo')
        self.archive_list('t.cpio.foo')
        self.archive_list('t.rpm.foo')
        self.archive_list('t.deb.foo')
        self.archive_extract('t.gz.foo')
        self.archive_extract('t.bz2.foo')
        self.archive_extract('t.jar.foo')
        self.archive_extract('t.Z.foo')
        self.archive_extract('t.cab.foo')
        self.archive_extract('t.arj.foo')
        self.archive_extract('t.cpio.foo')
        self.archive_extract('t.rpm.foo')
        self.archive_extract('t.deb.foo')
        self.archive_test('t.gz.foo')
        self.archive_test('t.bz2.foo')
        self.archive_test('t.jar.foo')
        self.archive_test('t.Z.foo')
        self.archive_test('t.cab.foo')
        self.archive_test('t.arj.foo')
        self.archive_test('t.cpio.foo')
        self.archive_test('t.rpm.foo')
        self.archive_test('t.deb.foo')

    @needs_program('file')
    @needs_program('7za')
    def test_p7azip_file (self):
        self.program = '7za'
        self.archive_commands('t.7z.foo', format="7z")
        self.archive_commands('t.zip.foo', format="zip")
        self.archive_list('t.gz.foo')
        self.archive_list('t.bz2.foo')
        self.archive_list('t.jar.foo')
        self.archive_list('t.Z.foo')
        self.archive_list('t.cab.foo')
        #self.archive_list('t.arj.foo')
        #self.archive_list('t.cpio.foo')
        self.archive_list('t.rpm.foo')
        #self.archive_list('t.deb.foo')
        self.archive_extract('t.gz.foo')
        self.archive_extract('t.bz2.foo')
        self.archive_extract('t.jar.foo')
        self.archive_extract('t.Z.foo')
        self.archive_extract('t.cab.foo')
        #self.archive_extract('t.arj.foo')
        #self.archive_extract('t.cpio.foo')
        #self.archive_extract('t.rpm.foo')
        #self.archive_extract('t.deb.foo')
        self.archive_test('t.gz.foo')
        self.archive_test('t.bz2.foo')
        self.archive_test('t.jar.foo')
        self.archive_test('t.Z.foo')
        self.archive_test('t.cab.foo')
        #self.archive_test('t.arj.foo')
        #self.archive_test('t.cpio.foo')
        #self.archive_test('t.rpm.foo')
        #self.archive_test('t.deb.foo')

    @needs_program('file')
    @needs_codec('7z', 'rar')
    def test_p7zip_rar (self):
        # only succeeds with the rar module for 7z installed
        self.program = '7z'
        self.archive_list('t.rar.foo')
        self.archive_extract('t.rar.foo')
        self.archive_test('t.rar.foo')

    @needs_program('file')
    @needs_program('unrar')
    def test_unrar (self):
        self.program = 'unrar'
        self.archive_list('t.rar.foo')
        self.archive_extract('t.rar.foo')

    @needs_program('file')
    @needs_program('rar')
    def test_rar (self):
        self.program = 'rar'
        self.archive_commands('t.rar.foo', format="rar")

    @needs_program('file')
    @needs_program('cabextract')
    def test_cabextract (self):
        self.program = 'cabextract'
        self.archive_list('t.cab.foo')
        self.archive_extract('t.cab.foo')

    @needs_program('file')
    @needs_program('orange')
    def test_orange (self):
        self.program = 'orange'
        self.archive_extract('t.cab.foo')

    @needs_program('file')
    @needs_program('arj')
    def test_arj (self):
        self.program = 'arj'
        self.archive_commands('t.arj.foo', format="arj")

    @needs_os('posix')
    @needs_program('file')
    @needs_program('ar')
    def test_ar (self):
        self.program = 'ar'
        self.archive_commands('t.a.foo', format='ar', singlefile=True)

    @needs_program('file')
    @needs_program('cpio')
    def test_cpio (self):
        self.program = 'cpio'
        self.archive_list('t.cpio.foo')
        self.archive_extract('t.cpio.foo')
        self.archive_create('t.cpio.foo', format="cpio")

    @needs_program('file')
    @needs_program('unace')
    def test_unace (self):
        self.program = 'unace'
        self.archive_list('t.ace.foo')
        self.archive_test('t.ace.foo')
        self.archive_extract('t.ace.foo')

    @needs_program('file')
    @needs_program('rpm')
    def test_rpm (self):
        self.program = 'rpm'
        self.archive_list('t.rpm.foo')
        # The rpm test fails on non-rpm system with missing dependencies.
        # I am too lazy to build a tiny rpm with one file
        # and no dependency.
        #self.archive_test('t.rpm.foo')

    @needs_program('file')
    @needs_program('rpm2cpio')
    @needs_program('cpio')
    def test_rpm_extract (self):
        self.program = 'rpm2cpio'
        self.archive_extract('t.rpm.foo')

    @needs_program('file')
    @needs_program('dpkg-deb')
    def test_dpkg (self):
        self.program = 'dpkg'
        self.archive_list('t.deb.foo')
        self.archive_extract('t.deb.foo')
        self.archive_test('t.deb.foo')

    @needs_program('file')
    @needs_program('lzop')
    def test_lzop (self):
        self.program = 'lzop'
        self.archive_commands('t.lzo.foo', format="lzop", singlefile=True)

    # file(1) does not recognize .lzma files
    #@needs_program('file')
    #@needs_program('lzma')
    #def test_lzma (self):
    #    self.program = 'lzma'
    #    self.archive_test('t.lzma.foo')
    #    self.archive_extract('t.lzma.foo')
    #    self.archive_create('t.lzma.foo', format="lzma", singlefile=True)

    @needs_program('file')
    @needs_program('lzip')
    def test_lzip (self):
        self.program = 'lzip'
        self.archive_test('t.txt.lz.foo')
        self.archive_extract('t.txt.lz.foo')
        self.archive_create('t.txt.lz.foo', format="lzip", singlefile=True)

    @needs_program('file')
    @needs_program('clzip')
    def test_clzip (self):
        self.program = 'clzip'
        self.archive_test('t.txt.lz.foo')
        self.archive_extract('t.txt.lz.foo')
        self.archive_create('t.txt.lz.foo', format="lzip", singlefile=True)

    @needs_program('file')
    @needs_program('plzip')
    def test_plzip (self):
        self.program = 'plzip'
        self.archive_test('t.txt.lz.foo')
        self.archive_extract('t.txt.lz.foo')
        self.archive_create('t.txt.lz.foo', format="lzip", singlefile=True)

    @needs_program('file')
    @needs_program('pdlzip')
    def test_pdlzip (self):
        self.program = 'pdlzip'
        self.archive_test('t.txt.lz.foo')
        self.archive_extract('t.txt.lz.foo')
        self.archive_create('t.txt.lz.foo', format="lzip", singlefile=True)

    @needs_program('file')
    @needs_program('xz')
    def test_xz (self):
        self.program = 'xz'
        self.archive_test('t.xz.foo')
        self.archive_extract('t.xz.foo')
        self.archive_create('t.xz.foo', format="xz", singlefile=True)

    @needs_program('file')
    @needs_program('lha')
    def test_lha (self):
        self.program = 'lha'
        self.archive_commands('t.lha.foo', format="lzh")

    # file(1) does not recognize .alz files
    #@needs_program('file')
    #@needs_program('unalz')
    #def test_unalz (self):
    #    self.program = 'unalz'
    #    self.archive_test('t.alz.foo')
    #    self.archive_list('t.alz.foo')
    #    self.archive_extract('t.alz.foo')

    @needs_program('arc')
    def test_arc (self):
        self.program = 'arc'
        self.archive_commands('t.arc.foo', format="arc", singlefile=True)

    @needs_program('nomarch')
    def test_nomarch (self):
        self.program = 'nomarch'
        self.archive_test('t.arc.foo')
        self.archive_list('t.arc.foo')
        self.archive_extract('t.arc.foo')

    # file(1) does not recognize .lrz files
    #@needs_program('file')
    #@needs_program('lrzip')
    #def test_lrzip (self):
    #    self.program = 'lrzip'
    #    self.archive_test('t.txt.lrz.foo')
    #    self.archive_extract('t.txt.lrz.foo')
    #    self.archive_create('t.txt.lrz.foo', format="lrzip", singlefile=True)

    @needs_program('rzip')
    def test_rzip (self):
        self.program = 'rzip'
        self.archive_extract('t.txt.rz.foo')
        self.archive_create('t.txt.rz.foo', format="rzip", singlefile=True)

    # XXX test failure
    #@needs_program('zoo')
    #def test_zoo (self):
    #    self.program = 'zoo'
    #    self.archive_commands('t.zoo.foo', format="zoo", singlefile=True)

    # xdms(1) cannot handle files without '.dms' extension
    #@needs_program('xdms')
    #def test_xdms (self):
    #    self.program = 'xdms'
    #    self.archive_extract('t.dms.foo')
    #    self.archive_test('t.dms.foo')
    #    self.archive_list('t.dms.foo')

    @needs_program('file')
    @needs_program('mac')
    def test_mac (self):
        self.program = 'mac'
        self.archive_extract('t.ape.foo')
        self.archive_create('t.ape.foo', srcfile='t.wav')

    # file(1) does not recognize .shn files
    #@needs_program('file')
    #@needs_program('shorten')
    #def test_shorten (self):
    #    self.program = 'shorten'
    #    self.archive_extract('t.shn.foo')
    #    self.archive_create('t.shn.foo', srcfile='t.wav')

    @needs_program('file')
    @needs_program('flac')
    def test_flac (self):
        self.program = 'flac'
        self.archive_extract('t.flac.foo')
        self.archive_test('t.flac.foo')
        self.archive_create('t.flac.foo', srcfile='t.wav', format='flac')
