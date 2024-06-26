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
"""Tests for utility functions"""

import unittest
import os
from patoolib import fileutil


class UtilTest(unittest.TestCase):
    """Test class for utility functions"""

    def test_samefile1(self):
        """Test is_same_file* with absolute paths"""
        filename1 = filename2 = __file__
        self.assertTrue(fileutil.is_same_filename(filename1, filename2))
        self.assertTrue(fileutil.is_same_file(filename1, filename2))

    def test_samefile2(self):
        """Test is_same_file* with relative paths"""
        parentdir = os.path.dirname(__file__)
        filename1 = os.path.dirname(parentdir)
        filename2 = os.path.join(parentdir, '..')
        self.assertTrue(fileutil.is_same_filename(filename1, filename2))
        self.assertTrue(fileutil.is_same_file(filename1, filename2))

    def test_samefile3(self):
        """Test is_same_file* with different files"""
        parentdir = os.path.dirname(__file__)
        filename1 = os.path.dirname(parentdir)
        filename2 = os.path.join(parentdir, '.')
        self.assertFalse(fileutil.is_same_file(filename1, filename2))
        self.assertFalse(fileutil.is_same_filename(filename1, filename2))

    def test_stripext(self):
        """Test stripext() with different filenames"""
        self.assertTrue(fileutil.stripext("bar.gz") == "bar")
        self.assertTrue(fileutil.stripext("foo/bar.tar.gz") == "bar")
        self.assertTrue(fileutil.stripext("foo/bartar.gz") == "bartar")
        self.assertTrue(fileutil.stripext("foo/bar.7z") == "bar")
        self.assertTrue(fileutil.stripext("foo/bar") == "bar")

    def test_rmtree(self):
        """Test rmtree() with non-existing and temporary dirs"""
        parentdir = os.path.dirname(__file__)
        nonexisting_dir = os.path.join(parentdir, "imadoofus")
        fileutil.rmtree(nonexisting_dir)
        existing_dir = fileutil.tmpdir()
        self.assertTrue(os.path.exists(existing_dir))
        with open(os.path.join(existing_dir, "t.txt"), "w") as f:
            f.write("42")
        fileutil.rmtree(existing_dir)
        self.assertFalse(os.path.exists(existing_dir))
