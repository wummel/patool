# Copyright (C) 2026 Bastian Kleineidam
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
import shutil
from patoolib import fileutil, cli
from . import basedir, datadir, needs_program


class ShellQuotingTest(unittest.TestCase):
    """Test extracting files with special characters."""

    @needs_program('gzip')
    def test_shell_quoting(self):
        """Extract files with special characters in the filename."""
        basename = "test_"
        for c in "&()^`'\t!%;$\\":
            self._extract(basename + c)

    def _extract(self, filename):
        """Run cli function to extract a gzip archive."""
        tmpdir_in = fileutil.tmpdir(dir=basedir)
        tmpdir_out = fileutil.tmpdir(dir=basedir)
        try:
            orig_archive = os.path.join(datadir, "t.txt.gz")
            archive = os.path.join(tmpdir_in, filename + ".gz")
            shutil.copy(orig_archive, archive)
            args = [
                "-vv",
                "--non-interactive",
                "extract",
                "--outdir",
                tmpdir_out,
                archive,
            ]
            cli.main(args=args)
        finally:
            fileutil.rmtree(tmpdir_in)
            fileutil.rmtree(tmpdir_out)
