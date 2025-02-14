# Copyright (C) 2010-2023 Bastian Kleineidam
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
"""Test mime detection"""

import unittest
import os
import patoolib
from . import needs_program, datadir


class TestMime(unittest.TestCase):
    """Test class for mime detection."""

    def mime_test(self, func, filename, mime, encoding, info):
        """Test that file has given mime and encoding as determined by
        given function.
        """
        file_mime, file_encoding = func(filename)
        fail_msg = "%s for archive `%s' should be %s, but was %s. Info: %s"
        if isinstance(mime, tuple):
            self.assertTrue(
                file_mime in mime,
                fail_msg % ("MIME type", filename, f"in {mime}", file_mime, info),
            )
        else:
            self.assertEqual(
                file_mime,
                mime,
                fail_msg % ("MIME type", filename, mime, file_mime, info),
            )
        self.assertEqual(
            file_encoding,
            encoding,
            fail_msg % ("Encoding", filename, encoding, file_encoding, info),
        )

    def mime_test_file(self, filename, mime, encoding=None):
        """Test that file has given mime and encoding as determined by
        file(1).
        """
        archive = os.path.join(datadir, filename)
        file_prog = patoolib.util.find_program("file")
        info = patoolib.mime.guess_mime_file_text(file_prog, archive)
        self.mime_test(patoolib.mime.guess_mime_file, archive, mime, encoding, info)

    def mime_test_mimedb(self, filename, mime, encoding=None):
        """Test that file has given mime and encoding as determined by the
        mimetypes module.
        """
        archive = os.path.join(datadir, filename)
        self.mime_test(patoolib.mime.guess_mime_mimedb, archive, mime, encoding, "")

    @needs_program('file')
    def test_mime_file(self):
        """Test mime detection of different archives with file(1)"""
        self.mime_test_file("t .7z", "application/x-7z-compressed")
        self.mime_test_file("t .cb7", "application/x-7z-compressed")
        self.mime_test_file("t.cb7.foo", "application/x-7z-compressed")
        self.mime_test_file("t.arj", "application/x-arj")
        self.mime_test_file("t.arj.foo", "application/x-arj")
        self.mime_test_file("t.txt.bz2", "application/x-bzip2")
        self.mime_test_file("t.txt.bz2.foo", "application/x-bzip2")
        # fails on ubuntu-latest github ci
        # self.mime_test_file("t.txt.bz3", "application/x-bzip3")
        # self.mime_test_file("t.txt.bz3.foo", "application/x-bzip3")
        self.mime_test_file("t.cab", "application/vnd.ms-cab-compressed")
        self.mime_test_file("t.cab.foo", "application/vnd.ms-cab-compressed")
        self.mime_test_file("t.cpio", "application/x-cpio")
        self.mime_test_file("t.cpio.foo", "application/x-cpio")
        self.mime_test_file("t.deb", "application/x-debian-package")
        self.mime_test_file("t.deb.foo", "application/x-debian-package")
        self.mime_test_file("t.txt.gz", "application/gzip")
        self.mime_test_file("t.txt.gz.foo", "application/gzip")
        self.mime_test_file("t.jar", "application/zip")
        self.mime_test_file("t.jar.foo", "application/zip")
        self.mime_test_file("t.txt.lzma", "application/x-lzma")
        self.mime_test_file("t.txt.lzma.foo", "application/x-lzma")
        self.mime_test_file("t.txt.lz", "application/x-lzip")
        self.mime_test_file("t.txt.lz.foo", "application/x-lzip")
        self.mime_test_file("t.txt.lzo", "application/x-lzop")
        self.mime_test_file("t.txt.lzo.foo", "application/x-lzop")
        self.mime_test_file("t.rar", "application/vnd.rar")
        self.mime_test_file("t.rar.foo", "application/vnd.rar")
        self.mime_test_file("t.cbr", "application/vnd.rar")
        self.mime_test_file("t.cbr.foo", "application/vnd.rar")
        self.mime_test_file("t.rpm", "application/x-rpm")
        self.mime_test_file("t.rpm.foo", "application/x-rpm")
        self.mime_test_file("t.tar", "application/x-tar")
        self.mime_test_file("t.tar.foo", "application/x-tar")
        self.mime_test_file("t.cbt", "application/x-tar")
        self.mime_test_file("t.cbt.foo", "application/x-tar")
        # fails on ubuntu-latest github ci
        # self.mime_test_file("t.tar.lz", "application/x-tar", "lzip")
        self.mime_test_file("t.tar.bz2", "application/x-tar", "bzip2")
        self.mime_test_file("t.tbz2", "application/x-tar", "bzip2")
        self.mime_test_file("t.tar.gz", "application/x-tar", "gzip")
        self.mime_test_file("t.taz", "application/x-tar", "gzip")
        self.mime_test_file("t.tgz", "application/x-tar", "gzip")
        # fails on windows-latest github ci
        # self.mime_test_file("t.tar.xz", "application/x-tar", "xz")
        # self.mime_test_file("t.tar.Z", "application/x-tar", "compress")
        # self.mime_test_file("t.tar.lzma", "application/x-tar", "lzma")
        # self.mime_test_file("t.tar.zst", "application/x-tar", "zstd")
        # file(1) cannot uncompress .lzma files
        # self.mime_test_file("t.tar.lzma.foo", "application/x-tar", "lzma")
        self.mime_test_file("t.txt.xz", "application/x-xz")
        self.mime_test_file("t.txt.xz.foo", "application/x-xz")
        self.mime_test_file("t.txt.Z", "application/x-compress")
        self.mime_test_file("t.txt.Z.foo", "application/x-compress")
        self.mime_test_file("t.txt.zst", "application/zstd")
        self.mime_test_file("t.txt.zst.foo", "application/zstd")
        self.mime_test_file("t.jar", "application/zip")
        self.mime_test_file("t.jar.foo", "application/zip")
        self.mime_test_file("t.zip", "application/zip")
        self.mime_test_file("t.zip.foo", "application/zip")
        self.mime_test_file("t.cbz", "application/zip")
        self.mime_test_file("t.cbz.foo", "application/zip")
        self.mime_test_file("t.ace", "application/x-ace")
        self.mime_test_file("t.ace.foo", "application/x-ace")
        self.mime_test_file("t.cba", "application/x-ace")
        self.mime_test_file("t.cba.foo", "application/x-ace")
        # fixme: test errors on windows
        # self.mime_test_file("t.txt.a", "application/x-archive")
        # self.mime_test_file("t.txt.a.foo", "application/x-archive")
        self.mime_test_file("t.lha", "application/x-lha")
        self.mime_test_file("t.lzh", "application/x-lha")
        self.mime_test_file("t.lha.foo", "application/x-lha")
        self.mime_test_file("t.alz", "application/x-alzip")
        self.mime_test_file("t.alz.foo", "application/x-alzip")
        self.mime_test_file("t.arc", "application/x-arc")
        self.mime_test_file("t.arc.foo", "application/x-arc")
        self.mime_test_file("t.txt.lz4", "application/x-lz4")
        self.mime_test_file("t.txt.lz4.foo", "application/x-lz4")
        self.mime_test_file("t.txt.lrz", "application/x-lrzip")
        self.mime_test_file("t.txt.lrz.foo", "application/x-lrzip")
        self.mime_test_file("t.txt.rz", "application/x-rzip")
        self.mime_test_file("t.txt.rz.foo", "application/x-rzip")
        self.mime_test_file("t.zoo", "application/x-zoo")
        self.mime_test_file("t.zoo.foo", "application/x-zoo")
        self.mime_test_file("t.dms", "application/x-dms")
        self.mime_test_file("t.dms.foo", "application/x-dms")
        self.mime_test_file("t.ape", "audio/x-ape")
        self.mime_test_file("t.ape.foo", "audio/x-ape")
        # file(1) does not recognize .shn files
        # self.mime_test_file("t.shn", "audio/x-shn")
        # self.mime_test_file("t.shn.foo", "audio/x-shn")
        self.mime_test_file("t.flac", "audio/flac")
        self.mime_test_file("t.flac.foo", "audio/flac")
        self.mime_test_file("t.adf", "application/x-adf")
        self.mime_test_file("t.adf.foo", "application/x-adf")
        self.mime_test_file("t.chm", "application/x-chm")
        self.mime_test_file("t.chm.foo", "application/x-chm")
        self.mime_test_file("t.iso", "application/x-iso9660-image")
        self.mime_test_file("t.epub", "application/zip")
        self.mime_test_file(
            "t.apk",
            (
                "application/zip",
                "application/java-archive",
                "application/jar",
                "application/vnd.android.package-archive",
            ),
        )
        self.mime_test_file("t.wim", "application/x-ms-wim")
        self.mime_test_file("t.wim.foo", "application/x-ms-wim")
        self.mime_test_file("t.zpaq", "application/zpaq")
        self.mime_test_file("t.zpaq.foo", "application/zpaq")

    # fixme: broken tests
    # @needs_program('file')
    # @needs_program('lzip')
    # def test_mime_file_lzip(self):
    #    self.mime_test_file("t.tar.lz.foo", "application/x-tar", "lzip")

    @needs_program('file')
    @needs_program('bzip2')
    def test_mime_file_bzip(self):
        """Test mime detection of TAR BZIP2 archives"""
        self.mime_test_file("t.tar.bz2.foo", "application/x-tar", "bzip2")
        self.mime_test_file("t.tbz2.foo", "application/x-tar", "bzip2")

    @needs_program('file')
    def test_nested_gzip(self):
        """Test mime detection of archives with double compression"""
        # We won't extract this with rar, as it doesn't support archives wrapped in gzip
        # compression, but we will recognize the archive as a gzip-wrapped rar-file
        self.mime_test_file("t.rar.gz", "application/vnd.rar", "gzip")
        self.mime_test_file("t.rar.gz.foo", "application/vnd.rar", "gzip")

    @needs_program('file')
    @needs_program('gzip')
    def test_mime_file_gzip(self):
        """Test mime detection of TAR GZIP archives"""
        self.mime_test_file("t.tar.gz.foo", "application/x-tar", "gzip")
        self.mime_test_file("t.taz.foo", "application/x-tar", "gzip")
        self.mime_test_file("t.tgz.foo", "application/x-tar", "gzip")

    # fixme: broken tests
    # @needs_program('file')
    # @needs_program('xz')
    # def test_mime_file_xzip(self):
    #    """Test mime detection of TAR XZ archives"""
    #    self.mime_test_file("t.tar.xz.foo", "application/x-tar", "xz")

    # fixme: broken tests
    # @needs_program("file")
    # @needs_program("zstd")
    # def test_mime_file_zstd(self):
    #    """Test mime detection of TAR ZSTD archives"""
    #    self.mime_test_file("t.tar.zst.foo", "application/x-tar", "zstd")

    # fixme: broken tests
    # @needs_program('file')
    # @needs_program('uncompress')
    # def test_mime_file_compress(self):
    #    """Test mime detection of TAR COMPRESS archives"""
    #    self.mime_test_file("t.tar.Z.foo", "application/x-tar", "compress")

    def test_mime_mimedb(self):
        """Test mime detection of different archives with mime DB"""
        self.mime_test_mimedb("t .7z", "application/x-7z-compressed")
        self.mime_test_mimedb("t .cb7", "application/x-7z-compressed")
        self.mime_test_mimedb("t.arj", "application/x-arj")
        self.mime_test_mimedb("t .bz2", "application/x-bzip2")
        self.mime_test_mimedb("t .bz3", "application/x-bzip3")
        self.mime_test_mimedb("t.cab", "application/x-cab")
        self.mime_test_mimedb("t.cbr", "application/vnd.rar")
        self.mime_test_mimedb("t.cpio", "application/x-cpio")
        self.mime_test_mimedb("t.deb", "application/x-debian-package")
        self.mime_test_mimedb("t.gz", "application/gzip")
        self.mime_test_mimedb("t.GZ", "application/gzip")
        self.mime_test_mimedb("t.jar", "application/java-archive")
        self.mime_test_mimedb("t.lzma", "application/x-lzma")
        self.mime_test_mimedb("t.txt.lz", "application/x-lzip")
        self.mime_test_mimedb("t.txt.lz4", "application/x-lz4")
        self.mime_test_mimedb("t.lzo", "application/x-lzop")
        self.mime_test_mimedb("t.rar", "application/vnd.rar")
        self.mime_test_mimedb("t.rpm", "application/x-rpm")
        self.mime_test_mimedb("t.tar", "application/x-tar")
        self.mime_test_mimedb("t.cbt", "application/x-tar")
        self.mime_test_mimedb("t.tar.bz2", "application/x-tar", "bzip2")
        self.mime_test_mimedb("t.tar.gz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.tar.lzma", "application/x-tar", "lzma")
        self.mime_test_mimedb("t.tar.xz", "application/x-tar", "xz")
        self.mime_test_mimedb("t.tar.lz", "application/x-tar", "lzip")
        self.mime_test_mimedb("t.tar.Z", "application/x-tar", "compress")
        self.mime_test_mimedb("t.tar.zst", "application/x-tar", "zstd")
        self.mime_test_mimedb("t.taz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.tbz2", "application/x-tar", "bzip2")
        self.mime_test_mimedb("t.tgz", "application/x-tar", "gzip")
        self.mime_test_mimedb("t.txt.gz", "application/gzip")
        self.mime_test_mimedb("t.txt.bz2", "application/x-bzip2")
        self.mime_test_mimedb("t.txt.bz3", "application/x-bzip3")
        self.mime_test_mimedb("t.txt.zst", "application/zstd")
        self.mime_test_mimedb("t .xz", "application/x-xz")
        self.mime_test_mimedb("t.Z", "application/x-compress")
        self.mime_test_mimedb(
            "t.zip", ("application/zip", "application/x-zip-compressed")
        )
        self.mime_test_mimedb(
            "t.cbz", ("application/zip", "application/x-zip-compressed")
        )
        self.mime_test_mimedb("t.ace", "application/x-ace")
        self.mime_test_mimedb("t.cba", "application/x-ace")
        self.mime_test_mimedb("t.a", "application/x-archive")
        self.mime_test_mimedb("t.lha", "application/x-lha")
        self.mime_test_mimedb("t.lzh", "application/x-lzh")
        self.mime_test_mimedb("t.alz", "application/x-alzip")
        self.mime_test_mimedb("t.arc", "application/x-arc")
        self.mime_test_mimedb("t.lrz", "application/x-lrzip")
        self.mime_test_mimedb("t.rz", "application/x-rzip")
        self.mime_test_mimedb("t.zoo", "application/x-zoo")
        self.mime_test_mimedb("t.dms", "application/x-dms")
        self.mime_test_mimedb("t.shar", "application/x-shar")
        self.mime_test_mimedb("t.ape", "audio/x-ape")
        self.mime_test_mimedb("t.shn", "audio/x-shn")
        self.mime_test_mimedb("t.flac", "audio/flac")
        self.mime_test_mimedb("t.adf", "application/x-adf")
        self.mime_test_mimedb("t.chm", "application/x-chm")
        self.mime_test_mimedb("t.iso", "application/x-iso9660-image")
        self.mime_test_mimedb("t.epub", "application/zip")
        self.mime_test_mimedb("t.apk", "application/zip")
        self.mime_test_mimedb("t.vhd", "application/x-vhd")
        self.mime_test_mimedb("t.wim", "application/x-ms-wim")
        self.mime_test_mimedb("t.zpaq", "application/zpaq")
