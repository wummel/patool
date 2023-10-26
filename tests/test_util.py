# -*- coding: utf-8 -*-
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
import unittest
import os
from patoolib import util

class UtilTest (unittest.TestCase):

    def test_samefile1 (self):
        filename1 = filename2 = __file__
        self.assertTrue(util.is_same_filename(filename1, filename2))
        self.assertTrue(util.is_same_file(filename1, filename2))

    def test_samefile2 (self):
        parentdir = os.path.dirname(__file__)
        filename1 = os.path.dirname(parentdir)
        filename2 = os.path.join(parentdir, '..')
        self.assertTrue(util.is_same_filename(filename1, filename2))
        self.assertTrue(util.is_same_file(filename1, filename2))

    def test_samefile3 (self):
        parentdir = os.path.dirname(__file__)
        filename1 = os.path.dirname(parentdir)
        filename2 = os.path.join(parentdir, '.')
        self.assertFalse(util.is_same_file(filename1, filename2))
        self.assertFalse(util.is_same_filename(filename1, filename2))

    def test_stripext(self):
        self.assertTrue(util.stripext("bar.gz") == "bar")
        self.assertTrue(util.stripext("foo/bar.tar.gz") == "bar")
        self.assertTrue(util.stripext("foo/bartar.gz") == "bartar")
        self.assertTrue(util.stripext("foo/bar.7z") == "bar")
        self.assertTrue(util.stripext("foo/bar") == "bar")


    def test_logging(self):
        msg = "this is a test message 💜"
        util.log_info(msg)
        util.log_error(msg)
        try:
            raise Exception(msg)
        except Exception:
            util.log_internal_error()
