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
"""Test patool diff command."""

import unittest
import os
from patoolib import cli
from . import datadir, needs_program


class ArchiveDiffTest(unittest.TestCase):
    """Test class for patool diff command."""

    @needs_program('diff')
    @needs_program('tar')
    @needs_program('unzip')
    def test_diff(self):
        """Run cli function to compare a TAR and ZIP archive."""
        archive1 = os.path.join(datadir, "t.tar")
        archive2 = os.path.join(datadir, "t.zip")
        args = ["-vv", "--non-interactive", "diff", archive1, archive2]
        cli.main(args=args)
