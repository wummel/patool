# -*- coding: utf-8 -*-
# Copyright (C) 2010 Bastian Kleineidam
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
from . import ArchiveTest, needs_cmd

class TestArchives (ArchiveTest):

    @needs_cmd('tar')
    def test_tar (self):
        self.tar_test('tar')

    @needs_cmd('star')
    def test_star (self):
        self.tar_test('star')

    def tar_test (self, cmd):
        self.archive_commands('t.tar', cmd)
        self.archive_commands('t.tar.gz', cmd)
        self.archive_commands('t.tar.Z', cmd)
        self.archive_commands('t.tar.bz2', cmd)
        self.archive_commands('t.tbz2', cmd)

    @needs_cmd('bzip2')
    def test_bzip2 (self):
        self.archive_extract('t.bz2', 'bzip2')
        self.archive_test('t.bz2', 'bzip2')
        self.archive_create('t.bz2', 'bzip2', singlefile=True)

    @needs_cmd('pbzip2')
    def test_pbzip2 (self):
        self.archive_extract('t.bz2', 'pbzip2')
        self.archive_test('t.bz2', 'pbzip2')
        self.archive_create('t.bz2', 'pbzip2', singlefile=True)

    @needs_cmd('echo')
    def test_echo (self):
        self.archive_list('t.bz2', 'echo')
        self.archive_list('t.Z', 'echo')

    @needs_cmd('unzip')
    def test_unzip (self):
        self.archive_extract('t.zip', 'unzip')
        self.archive_list('t.zip', 'unzip')
        self.archive_test('t.zip', 'unzip')
        self.archive_extract('t.jar', 'unzip')
        self.archive_list('t.jar', 'unzip')
        self.archive_test('t.jar', 'unzip')

    @needs_cmd('gzip')
    def test_gzip (self):
        self.archive_commands('t.gz', 'gzip', singlefile=True)
        self.archive_commands('t.txt.gz', 'gzip', singlefile=True)
        self.archive_extract('t.Z', 'gzip')

    @needs_cmd('uncompress.real')
    def test_uncompress (self):
        self.archive_extract('t.Z', 'uncompress.real')

    @needs_cmd('compress')
    def test_compress (self):
        self.archive_create('t.Z', 'compress', singlefile=True)

    @needs_cmd('7z')
    def test_p7zip (self):
        self.archive_commands('t.7z', '7z')
        self.archive_list('t.gz', '7z')
        self.archive_list('t.bz2', '7z')
        self.archive_list('t.zip', '7z')
        self.archive_list('t.jar', '7z')
        self.archive_list('t.Z', '7z')
        self.archive_list('t.rar', '7z')
        self.archive_list('t.cab', '7z')
        self.archive_list('t.arj', '7z')
        self.archive_list('t.cpio', '7z')
        self.archive_list('t.rpm', '7z')
        self.archive_list('t.deb', '7z')
        self.archive_extract('t.gz', '7z')
        self.archive_extract('t.bz2', '7z')
        self.archive_extract('t.zip', '7z')
        self.archive_extract('t.jar', '7z')
        self.archive_extract('t.Z', '7z')
        self.archive_extract('t.rar', '7z')
        self.archive_extract('t.cab', '7z')
        self.archive_extract('t.arj', '7z')
        self.archive_extract('t.cpio', '7z')
        self.archive_extract('t.rpm', '7z')
        self.archive_extract('t.deb', '7z')
        self.archive_test('t.gz', '7z')
        self.archive_test('t.bz2', '7z')
        self.archive_test('t.zip', '7z')
        self.archive_test('t.jar', '7z')
        self.archive_test('t.Z', '7z')
        self.archive_test('t.rar', '7z')
        self.archive_test('t.cab', '7z')
        self.archive_test('t.arj', '7z')
        self.archive_test('t.cpio', '7z')
        self.archive_test('t.rpm', '7z')
        self.archive_test('t.deb', '7z')

    @needs_cmd('unrar')
    def test_unrar (self):
        self.archive_list('t.rar', 'unrar')
        self.archive_extract('t.rar', 'unrar')

    @needs_cmd('rar')
    def test_rar (self):
        self.archive_commands('t.rar', 'rar')

    @needs_cmd('cabextract')
    def test_cabextract (self):
        self.archive_list('t.cab', 'cabextract')
        self.archive_extract('t.cab', 'cabextract')

    @needs_cmd('arj')
    def test_arj (self):
        self.archive_commands('t.arj', 'arj')

    @needs_cmd('cpio')
    def test_cpio (self):
        self.archive_list('t.cpio', 'cpio')
        self.archive_extract('t.cpio', 'cpio')
        self.archive_create('t.cpio', 'cpio')

    @needs_cmd('rpm')
    def test_rpm (self):
        self.archive_list('t.rpm', 'rpm')
        # the rpm test fails on non-rpm system with missing dependencies
        #self.archive_test('t.rpm', 'rpm')

    @needs_cmd('rpm2cpio')
    @needs_cmd('cpio')
    def test_rpm_extract (self):
        self.archive_extract('t.rpm', 'rpm2cpio')

    @needs_cmd('dpkg-deb')
    def test_dpkg (self):
        self.archive_list('t.deb', 'dpkg')
        self.archive_extract('t.deb', 'dpkg')
        self.archive_test('t.deb', 'dpkg')

    @needs_cmd('lzop')
    def test_lzop (self):
        self.archive_commands('t.lzo', 'lzop', singlefile=True)

