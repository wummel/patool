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
"""Test patool repack command"""

import unittest
import os
from patoolib import fileutil, cli
from . import datadir, needs_program, needs_one_program


class ArchiveRepackTest(unittest.TestCase):
    """Test class for patool repack command"""

    def repack(self, name1, name2):
        """Repack archive with name1 to archive with name2."""
        archive1 = os.path.join(datadir, name1)
        tmpdir = fileutil.tmpdir()
        try:
            archive2 = os.path.join(tmpdir, name2)
            args = ["-vv", "--non-interactive", "repack", archive1, archive2]
            cli.main(args=args)
            args = ["--non-interactive", "diff", archive1, archive2]
            cli.main(args=args)
        finally:
            fileutil.rmtree(tmpdir)

    @needs_program('diff')
    @needs_one_program(('tar', 'star', '7z'))
    @needs_one_program(('zip', '7z'))
    def test_repack(self):
        """Test repacking a TAR file to a ZIP file."""
        self.repack('t.tar', 't.zip')

    @needs_program('diff')
    @needs_one_program(('gzip', '7z'))
    @needs_one_program(('bzip2', '7z'))
    def test_repack_same_format_different_compression(self):
        """Test repacking a GZIP TAR file to a BZIP2 TAR file."""
        self.repack('t.tar.gz', 't.tar.bz2')

    @needs_program('diff')
    def test_repack_same_format(self):
        """Test repacking a ZIP and GZIP TAR file in the same format."""
        self.repack('t.tar.gz', 't1.tar.gz')
        self.repack('t.zip', 't1.zip')
