# Copyright (C) 2013-2023 Bastian Kleineidam
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
"""Test patool search command"""

import unittest
import os
from patoolib import cli
from . import datadir, needs_program


class ArchiveSearchTest(unittest.TestCase):
    """Test class for patool search command"""

    @needs_program('grep')
    @needs_program('tar')
    def test_search_tar(self):
        """Run cli function to search in TAR archive."""
        pattern = "42"
        archive = os.path.join(datadir, "t.tar")
        self.search(pattern, archive)

    @needs_program('grep')
    @needs_program('unzip')
    def test_search_zip(self):
        """Run cli function to search in ZIP archive."""
        pattern = "42"
        archive = os.path.join(datadir, "t.zip")
        self.search(pattern, archive)

    def search(self, pattern, archive):
        """Utility function to run the cli search"""
        args = ["-vv", "--non-interactive", "search", pattern, archive]
        cli.main(args=args)
