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
"""Test patool command line parsing."""

import unittest
import pytest
from patoolib import cli


class ArchiveCliTest(unittest.TestCase):
    """Test class for patool command line options."""

    def test_cli_verbosity(self):
        """Test cli verbosity options"""
        parser = cli.create_argparser()
        args = ["extract", "t.zip"]
        pargs = parser.parse_args(args=args)
        self.assertEqual(pargs.verbosity, 0)
        args = ["-v", "extract", "t.zip"]
        pargs = parser.parse_args(args=args)
        self.assertEqual(pargs.verbosity, 1)
        args = ["-vv", "extract", "t.zip"]
        pargs = parser.parse_args(args=args)
        self.assertEqual(pargs.verbosity, 2)
        args = ["-q", "extract", "t.zip"]
        pargs = parser.parse_args(args=args)
        self.assertEqual(pargs.quiet, 1)
        args = ["-qq", "extract", "t.zip"]
        pargs = parser.parse_args(args=args)
        self.assertEqual(pargs.quiet, 2)
        # conflicting options
        with pytest.raises(SystemExit):
            args = ["-qv", "extract", "t.zip"]
            pargs = parser.parse_args(args=args)
