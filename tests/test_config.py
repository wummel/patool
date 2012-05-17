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
import patoolib

class TestConfiguration (unittest.TestCase):

    def test_archive_mimetypes (self):
        # test that each format has a MIME type
        self.assertEqual(set(patoolib.ArchiveFormats),
                         set(patoolib.ArchiveMimetypes.values()))

    def test_archive_programs (self):
        # test that the key is an archive format
        self.assertEqual(set(patoolib.ArchiveFormats),
                         set(patoolib.ArchivePrograms.keys()))
        for commands in patoolib.ArchivePrograms.values():
            for command in commands:
                if command is not None:
                    self.assertTrue(command in patoolib.ArchiveCommands)

    def test_compression_programs (self):
        self.assertTrue(set(patoolib.ArchiveCompressions).issubset(
                         set(patoolib.ArchiveFormats)))

    def test_encoding_mimes (self):
        self.assertEqual(set(patoolib.ArchiveCompressions),
                         set(patoolib.util.Encoding2Mime.keys()))
        for mime in patoolib.util.Encoding2Mime.values():
            self.assertTrue(mime in patoolib.ArchiveMimetypes)

    def test_filetext_mime (self):
        for mime in patoolib.util.FileText2Mime.values():
            self.assertTrue(mime in patoolib.ArchiveMimetypes)
