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
"""Test patool extract command."""

import unittest
import os
from patoolib import fileutil, cli
from . import basedir, datadir, needs_program


class ArchiveExtractTest(unittest.TestCase):
    """Test class for patool extract command."""

    @needs_program('7z')
    def test_extract(self):
        """Run cli function to extract a 7Z archive."""
        tmpdir = fileutil.tmpdir(dir=basedir)
        try:
            archive = os.path.join(datadir, "t .7z")
            args = ["-vv", "--non-interactive", "extract", "--outdir", tmpdir, archive]
            cli.main(args=args)
        finally:
            fileutil.rmtree(tmpdir)
