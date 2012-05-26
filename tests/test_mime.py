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
import unittest
import os
import patoolib
from . import needs_program, datadir


class TestMime (unittest.TestCase):

    def mime_test (self, func, filename, mime, encoding):
        """Test that file has given mime and encoding as determined by
        given function."""
        archive = os.path.join(datadir, filename)
        file_mime, file_encoding = func(archive)
        fail_msg = "%s for archive `%s' should be %s, but was %s"
        if isinstance(mime, tuple):
            self.assertTrue(file_mime in mime, fail_msg % ("MIME type", filename, "in %s" % str(mime), file_mime))
        else:
            self.assertEqual(file_mime, mime, fail_msg % ("MIME type", filename, mime, file_mime))
        self.assertEqual(file_encoding, encoding, fail_msg % ("Encoding", filename, encoding, file_encoding))

    def mime_test_file (self, filename, mime, encoding):
        """Test that file has given mime and encoding as determined by
        file(1)."""
        self.mime_test(patoolib.util.guess_mime_file, filename, mime, encoding)

    def mime_test_mimedb (self, filename, mime, encoding):
        """Test that file has given mime and encoding as determined by the
        mimetypes module."""
        self.mime_test(patoolib.util.guess_mime_mimedb, filename, mime, encoding)

    @needs_program('file')
    def test_mime_file (self):
        self.mime_test_file("t .7z", "application/x-7z-compressed", None)
        self.mime_test_file("t.7z.foo", "application/x-7z-compressed", None)
        self.mime_test_file("t.arj", "application/x-arj", None)
        self.mime_test_file("t.arj.foo", "application/x-arj", None)
        self.mime_test_file("t.txt.bz2", "application/x-bzip2", None)
        self.mime_test_file("t.txt.bz2.foo", "application/x-bzip2", None)
        self.mime_test_file("t.cab", "application/vnd.ms-cab-compressed", None)
        self.mime_test_file("t.cab.foo", "application/vnd.ms-cab-compressed", None)
        self.mime_test_file("t.cpio", "application/x-cpio", None)
        self.mime_test_file("t.cpio.foo", "application/x-cpio", None)
        self.mime_test_file("t.deb", "application/x-debian-package", None)
        self.mime_test_file("t.deb.foo", "application/x-debian-package", None)
        self.mime_test_file("t.txt.gz", "application/x-gzip", None)
        self.mime_test_file("t.txt.gz.foo", "application/x-gzip", None)
        self.mime_test_file("t.jar", "application/zip", None)
        self.mime_test_file("t.jar.foo", "application/zip", None)
        # file(1) does not recognize .lzma files
        #self.mime_test_file("t.lzma", "application/x-lzma", None)
        #self.mime_test_file("t.lzma.foo", "application/x-lzma", None)
        self.mime_test_file("t.txt.lz", "application/x-lzip", None)
        self.mime_test_file("t.txt.lz.foo", "application/x-lzip", None)
        self.mime_test_file("t.lzo", "application/x-lzop", None)
        self.mime_test_file("t.lzo.foo", "application/x-lzop", None)
        self.mime_test_file("t.rar", "application/x-rar", None)
        self.mime_test_file("t.rar.foo", "application/x-rar", None)
        self.mime_test_file("t.rpm", "application/x-rpm", None)
        self.mime_test_file("t.rpm.foo", "application/x-rpm", None)
        self.mime_test_file("t.tar", "application/x-tar", None)
        self.mime_test_file("t.tar.foo", "application/x-tar", None)
        self.mime_test_file("t.tar.lz", "application/x-tar", "lzip")
        self.mime_test_file("t.tar.bz2", "application/x-tar", "bzip2")
        self.mime_test_file("t.tbz2", "application/x-tar", "bzip2")
        self.mime_test_file("t.tar.gz", "application/x-tar", "gzip")
        self.mime_test_file("t.taz", "application/x-tar", "gzip")
        self.mime_test_file("t.tgz", "application/x-tar", "gzip")
        self.mime_test_file("t.tar.xz", "application/x-tar", "xz")
        self.mime_test_file("t.tar.Z", "application/x-tar", "compress")
        # file(1) does not recognize .lzma files
        #self.mime_test_file("t.tar.lzma", "application/x-tar", "lzma")
        #self.mime_test_file("t.tar.lzma.foo", "application/x-tar", "lzma")
        self.mime_test_file("t.txt.gz", "application/x-gzip", None)
        self.mime_test_file("t.txt.gz.foo", "application/x-gzip", None)
        self.mime_test_file("t.txt.xz", "application/x-xz", None)
        self.mime_test_file("t.txt.xz.foo", "application/x-xz", None)
        self.mime_test_file("t.txt.Z", "application/x-compress", None)
        self.mime_test_file("t.txt.Z.foo", "application/x-compress", None)
        self.mime_test_file("t.jar", "application/zip", None)
        self.mime_test_file("t.jar.foo", "application/zip", None)
        self.mime_test_file("t.zip", "application/zip", None)
        self.mime_test_file("t.zip.foo", "application/zip", None)
        self.mime_test_file("t.ace", "application/x-ace", None)
        self.mime_test_file("t.ace.foo", "application/x-ace", None)
        self.mime_test_file("t.txt.a", "application/x-archive", None)
        self.mime_test_file("t.txt.a.foo", "application/x-archive", None)
        self.mime_test_file("t.lha", "application/x-lha", None)
        self.mime_test_file("t.lzh", "application/x-lha", None)
        self.mime_test_file("t.lha.foo", "application/x-lha", None)
        # file(1) does not recognize .alz files
        #self.mime_test_file("t.alz", "application/x-alzip", None)
        #self.mime_test_file("t.alz.foo", "application/x-alzip", None)
        self.mime_test_file("t.arc", "application/x-arc", None)
        self.mime_test_file("t.arc.foo", "application/x-arc", None)
        # file(1) does not recognize .lrz files
        #self.mime_test_file("t.txt.lrz", "application/x-lrzip", None)
        #self.mime_test_file("t.txt.lrz.foo", "application/x-lrzip", None)
        self.mime_test_file("t.txt.rz", "application/x-rzip", None)
        self.mime_test_file("t.txt.rz.foo", "application/x-rzip", None)
        self.mime_test_file("t.zoo", "application/x-zoo", None)
        self.mime_test_file("t.zoo.foo", "application/x-zoo", None)
        self.mime_test_file("t.dms", "application/x-dms", None)
        self.mime_test_file("t.dms.foo", "application/x-dms", None)
        self.mime_test_file("t.ape", "audio/x-ape", None)
        self.mime_test_file("t.ape.foo", "audio/x-ape", None)
        # file(1) does not recognize .shn files
        #self.mime_test_file("t.shn", "audio/x-shn", None)
        #self.mime_test_file("t.shn.foo", "audio/x-shn", None)
        self.mime_test_file("t.flac", "audio/flac", None)
        self.mime_test_file("t.flac.foo", "audio/flac", None)

    @needs_program('file')
    @needs_program('lzip')
    def test_mime_file_lzip (self):
        self.mime_test_file("t.tar.lz.foo", "application/x-tar", "lzip")

    @needs_program('file')
    @needs_program('bzip2')
    def test_mime_file_bzip (self):
        self.mime_test_file("t.tar.bz2.foo", "application/x-tar", "bzip2")
        self.mime_test_file("t.tbz2.foo", "application/x-tar", "bzip2")

    @needs_program('file')
    @needs_program('gzip')
    def test_mime_file_gzip (self):
        self.mime_test_file("t.tar.gz.foo", "application/x-tar", "gzip")
        self.mime_test_file("t.taz.foo", "application/x-tar", "gzip")
        self.mime_test_file("t.tgz.foo", "application/x-tar", "gzip")

    @needs_program('file')
    @needs_program('xz')
    def test_mime_file_xzip (self):
        self.mime_test_file("t.tar.xz.foo", "application/x-tar", "xz")

    @needs_program('file')
    @needs_program('uncompress')
    def test_mime_file_compress (self):
        self.mime_test_file("t.tar.Z.foo", "application/x-tar", "compress")

    def test_mime_mimedb (self):
        self.mime_test_mimedb("t .7z", "application/x-7z-compressed", None)
        self.mime_test_mimedb("t.arj", "application/x-arj", None)
        self.mime_test_mimedb("t .bz2", "application/x-bzip2", None)
        self.mime_test_mimedb("t.cab", "application/x-cab", None)
        self.mime_test_mimedb("t.cpio", "application/x-cpio", None)
        self.mime_test_mimedb("t.deb", "application/x-debian-package", None)
        self.mime_test_mimedb("t.gz", "application/x-gzip", None)
        self.mime_test_mimedb("t.jar", "application/java-archive", None)
        self.mime_test_mimedb("t.lzma", "application/x-lzma", None)
        self.mime_test_mimedb("t.txt.lz", "application/x-lzip", None)
        self.mime_test_mimedb("t.lzo", "application/x-lzop", None)
        self.mime_test_mimedb("t.rar", ("application/rar", "application/x-rar"), None)
        self.mime_test_mimedb("t.rpm", ("application/x-redhat-package-manager", "application/x-rpm"), None)
        self.mime_test_mimedb("t.tar", "application/x-tar", None)
        self.mime_test_mimedb("t.tar.bz2", "application/x-tar", "bzip2")
        self.mime_test_mimedb("t.tar.gz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.tar.lzma", "application/x-tar", "lzma")
        self.mime_test_mimedb("t.tar.xz", "application/x-tar", "xz")
        self.mime_test_mimedb("t.tar.lz", "application/x-tar", "lzip")
        self.mime_test_mimedb("t.tar.Z", "application/x-tar", "compress")
        self.mime_test_mimedb("t.taz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.tbz2", "application/x-tar", "bzip2")
        self.mime_test_mimedb("t.tgz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.txt.gz", "application/x-gzip", None)
        self.mime_test_mimedb("t .xz", "application/x-xz", None)
        self.mime_test_mimedb("t.Z", "application/x-compress", None)
        self.mime_test_mimedb("t.zip", ("application/zip", "application/x-zip-compressed"), None)
        self.mime_test_mimedb("t.ace", "application/x-ace", None)
        self.mime_test_mimedb("t.a", "application/x-archive", None)
        self.mime_test_mimedb("t.lha", "application/x-lha", None)
        self.mime_test_mimedb("t.lzh", "application/x-lzh", None)
        self.mime_test_mimedb("t.alz", "application/x-alzip", None)
        self.mime_test_mimedb("t.arc", "application/x-arc", None)
        self.mime_test_mimedb("t.lrz", "application/x-lrzip", None)
        self.mime_test_mimedb("t.rz", "application/x-rzip", None)
        self.mime_test_mimedb("t.zoo", "application/x-zoo", None)
        self.mime_test_mimedb("t.dms", "application/x-dms", None)
        self.mime_test_mimedb("t.shar", "application/x-shar", None)
        self.mime_test_mimedb("t.ape", "audio/x-ape", None)
        self.mime_test_mimedb("t.shn", "audio/x-shn", None)
        self.mime_test_mimedb("t.flac", "audio/flac", None)
