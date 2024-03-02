# Copyright (C) 2023 Bastian Kleineidam
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
"""Test the jar program"""
from . import ArchiveTest
from .. import needs_program


class TestJar(ArchiveTest):
    """Test class for the jar program"""

    program = "jar"

    @needs_program(program)
    def test_jar(self):
        """Extract and list different ZIP archives."""
        self.archive_extract("t.zip", check=None)
        self.archive_list("t.zip")
        self.archive_extract("t.cbz", check=None)
        self.archive_list("t.cbz")
        self.archive_extract("t.apk", check=None)
        self.archive_list("t.apk")
        self.archive_extract("t.jar", check=None)
        self.archive_list("t.jar")
        self.archive_extract("t.epub", check=None)
        self.archive_list("t.epub")

    @needs_program("file")
    @needs_program(program)
    def test_jar_file(self):
        """Extract and list different renamed ZIP archives."""
        self.archive_extract("t.zip.foo", check=None)
        self.archive_list("t.zip.foo")
        self.archive_extract("t.cbz.foo", check=None)
        self.archive_list("t.cbz.foo")
        self.archive_extract("t.apk.foo", check=None)
        self.archive_list("t.apk.foo")
        self.archive_extract("t.jar.foo", check=None)
        self.archive_list("t.jar.foo")
        self.archive_extract("t.epub.foo", check=None)
        self.archive_list("t.epub.foo")
