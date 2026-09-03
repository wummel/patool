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
"""Test utility functions"""

import unittest
from patoolib import log, util


class UtilTest(unittest.TestCase):
    """Test class for utility functions"""

    def test_logging(self):
        """Test log.log_*() functions"""
        msg = "this is a test info message 💜"
        log.log_info(msg)
        msg = "this is a test error message 💜"
        log.log_error(msg)
        try:
            raise Exception(msg)
        except Exception as exc:
            log.log_internal_error(exc)

    def test_quote_unix(self):
        """Test util.shell_quote_unix()"""
        self.assertEqual(util.shell_quote_unix("a b"), "'a b'")

    def test_quote_nt(self):
        """Test util.shell_quote_nt()"""
        self.assertEqual(util.shell_quote_nt("a b"), '"a b"')
        for c in '&()^!':
            self.assertEqual(util.shell_quote_nt(f"a{c}{c} b"), f'"a{c}{c} b"')
        for c in '"<>|?*\n':
            self.assertRaises(ValueError, util.shell_quote_nt, c)
        self.assertEqual(util.shell_quote_nt("a%USER%b"), '"a%%USER%%b"')

    def test_strlist_with_or(self):
        """Test util.strlist()"""
        alist = []
        self.assertEqual(util.strlist_with_or(alist), "")
        alist = ["test1"]
        self.assertEqual(util.strlist_with_or(alist), "test1")
        alist = ["test1", "test2"]
        self.assertEqual(util.strlist_with_or(alist), "test1 or test2")
        alist = ["test1", "test2", "test3"]
        self.assertEqual(util.strlist_with_or(alist), "test1, test2 or test3")
