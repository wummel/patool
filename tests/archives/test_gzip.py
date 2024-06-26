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
"""Test the gzip program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestGzip(ArchiveTest):
    """Test class for the gzip program"""

    program = 'gzip'

    @needs_program(program)
    def test_gzip(self):
        """Run archive commands with GZIP and COMPRESS archive."""
        self.archive_commands('t.txt.gz', check=Content.Singlefile)
        self.archive_extract('t.txt.Z', check=Content.Singlefile)

    @needs_program('file')
    @needs_program(program)
    def test_gzip_file(self):
        """Run archive commands with renamed GZIP and COMPRESS archive."""
        self.archive_commands(
            't.txt.gz.foo', skip_create=True, check=Content.Singlefile
        )
        self.archive_extract('t.txt.Z.foo', check=Content.Singlefile)

    def get_expected_singlefile_output(self, archive):
        """Gzip restores the original filename for .gz files"""
        if archive.endswith(".Z.foo"):
            return "t.txt.Z"
        return "t.txt"
