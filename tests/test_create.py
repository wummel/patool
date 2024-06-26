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
"""Test patool create command."""

import unittest
import os
from patoolib import cli, fileutil
from . import basedir, datadir, needs_program


class ArchiveCreateTest(unittest.TestCase):
    """Test class for patool create command."""

    @needs_program('7z')
    def test_create(self):
        """Run cli function to create a 7Z archive."""
        tmpdir = fileutil.tmpdir(dir=basedir)
        try:
            files = [os.path.join(datadir, "t"), os.path.join(datadir, "t.txt")]
            archive = os.path.join(tmpdir, "t.7z")
            args = ["-vv", "--non-interactive", "create", archive]
            args.extend(files)
            cli.main(args=args)
        finally:
            fileutil.rmtree(tmpdir)
