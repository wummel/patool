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
import unittest
import os
import patoolib
from tests import needs_program, datadir


class TestMime (unittest.TestCase):

    def mime_test (self, filename, mime, encoding):
        """Test that file has given mime and encoding."""
        archive = os.path.join(datadir, filename)
        res = patoolib.util.guess_mime(archive)
        fail_msg = "MIME type for archive `%s' should be (%s, %s), but was %s" % (filename, mime, encoding, res)
        self.assertEqual(res, (mime, encoding), fail_msg)

    @needs_program('file')
    def test_mime (self):
        self.mime_test("t.7z", "application/x-7z-compressed", None)
        self.mime_test("t.7z.foo", "application/x-7z-compressed", None)
        self.mime_test("t.arj", "application/x-arj", None)
        self.mime_test("t.arj.foo", "application/x-arj", None)
        self.mime_test("t.bz2", "application/x-bzip2", None)
        self.mime_test("t.bz2.foo", "application/x-bzip2", None)
        self.mime_test("t.cab", "application/vnd.ms-cab-compressed", None)
        self.mime_test("t.cab.foo", "application/vnd.ms-cab-compressed", None)
        self.mime_test("t.cpio", "application/x-cpio", None)
        self.mime_test("t.cpio.foo", "application/x-cpio", None)
        self.mime_test("t.deb", "application/x-debian-package", None)
        self.mime_test("t.deb.foo", "application/x-debian-package", None)
        self.mime_test("t.gz", "application/x-gzip", None)
        self.mime_test("t.gz.foo", "application/x-gzip", None)
        self.mime_test("t.jar", "application/zip", None)
        self.mime_test("t.jar.foo", "application/zip", None)
        self.mime_test("t.lzma", "application/x-lzma", None)
        # file(1) does not recognize .lzma files
        #self.mime_test("t.lzma.foo", "application/x-lzma", None)
        self.mime_test("t.txt.lz", "application/x-lzip", None)
        self.mime_test("t.txt.lz.foo", "application/x-lzip", None)
        self.mime_test("t.lzo", "application/x-lzop", None)
        self.mime_test("t.lzo.foo", "application/x-lzop", None)
        self.mime_test("t.rar", "application/x-rar", None)
        self.mime_test("t.rar.foo", "application/x-rar", None)
        self.mime_test("t.rpm", "application/x-rpm", None)
        self.mime_test("t.rpm.foo", "application/x-rpm", None)
        self.mime_test("t.tar", "application/x-tar", None)
        self.mime_test("t.tar.foo", "application/x-tar", None)
        self.mime_test("t.tar.bz2", "application/x-tar", "bzip2")
        self.mime_test("t.tar.bz2.foo", "application/x-tar", "bzip2")
        self.mime_test("t.tar.gz", "application/x-tar", "gzip")
        self.mime_test("t.tar.gz.foo", "application/x-tar", "gzip")
        self.mime_test("t.tar.lzma", "application/x-tar", "lzma")
        # file(1) does not recognize .lzma files
        #self.mime_test("t.tar.lzma.foo", "application/x-tar", "lzma")
        self.mime_test("t.tar.xz", "application/x-tar", "xz")
        self.mime_test("t.tar.xz.foo", "application/x-tar", "xz")
        self.mime_test("t.tar.lz", "application/x-tar", "lzip")
        self.mime_test("t.tar.lz.foo", "application/x-tar", "lzip")
        self.mime_test("t.tar.Z", "application/x-tar", "compress")
        self.mime_test("t.tar.Z.foo", "application/x-tar", "compress")
        self.mime_test("t.taz", "application/x-tar", "compress")
        self.mime_test("t.taz.foo", "application/x-tar", "compress")
        self.mime_test("t.tbz2", "application/x-tar", "bzip2")
        self.mime_test("t.tbz2.foo", "application/x-tar", "bzip2")
        self.mime_test("t.tgz", "application/x-tar", "gzip")
        self.mime_test("t.tgz.foo", "application/x-tar", "gzip")
        self.mime_test("t.txt.gz", "application/x-gzip", None)
        self.mime_test("t.txt.gz.foo", "application/x-gzip", None)
        self.mime_test("t.xz", "application/x-xz", None)
        self.mime_test("t.xz.foo", "application/x-xz", None)
        self.mime_test("t.Z", "application/x-compress", None)
        self.mime_test("t.Z.foo", "application/x-compress", None)
        self.mime_test("t.zip", "application/zip", None)
        self.mime_test("t.zip.foo", "application/zip", None)
        self.mime_test("t.ace", "application/x-ace", None)
        self.mime_test("t.ace.foo", "application/x-ace", None)
