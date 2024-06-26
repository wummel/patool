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
"""Test patool configuration values"""

import unittest
import patoolib


class TestConfiguration(unittest.TestCase):
    """Test class for patool configuration values"""

    def test_archive_mimetypes(self):
        """Test that each format has a MIME type"""
        self.assertEqual(
            set(patoolib.ArchiveFormats), set(patoolib.ArchiveMimetypes.values())
        )

    def test_archive_programs(self):
        """Test that the archive program key is an archive format"""
        self.assertEqual(
            set(patoolib.ArchiveFormats), set(patoolib.ArchivePrograms.keys())
        )
        for commands in patoolib.ArchivePrograms.values():
            for command in commands:
                if command is not None:
                    self.assertTrue(command in patoolib.ArchiveCommands)
            for programs in commands.values():
                self.assertTrue(isinstance(programs, tuple))

    def test_compression_programs(self):
        """Test that compressions are archive formats"""
        self.assertTrue(
            set(patoolib.ArchiveCompressions).issubset(set(patoolib.ArchiveFormats))
        )

    def test_encoding_mimes_keys(self):
        """Test that all compressions have a mime type"""
        self.assertEqual(
            set(patoolib.ArchiveCompressions), set(patoolib.mime.Encoding2Mime.keys())
        )

    def test_encoding_mimes_values(self):
        """Test that all encoding mimes are known mime types"""
        for mime in patoolib.mime.Encoding2Mime.values():
            self.assertTrue(mime in patoolib.ArchiveMimetypes)

    def test_filetext_mime(self):
        """Test that all text mime values are known mime types"""
        for mime in patoolib.mime.FileText2Mime.values():
            self.assertTrue(mime in patoolib.ArchiveMimetypes)
