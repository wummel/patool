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
"""Test the pigz program"""

from . import ArchiveTest, Content
from .. import needs_program


class TestPigz(ArchiveTest):
    """Test class for the pigz program"""

    program = 'pigz'

    @needs_program(program)
    def test_pigz(self):
        """Run archive commands with GZIP archive."""
        self.archive_commands('t.txt.gz', check=Content.Singlefile)

    @needs_program('file')
    @needs_program(program)
    def test_pigz_file(self):
        """Run archive commands with renamed GZIP archive."""
        self.archive_commands(
            't.txt.gz.foo', check=Content.Singlefile, skip_create=True, skip_test=True
        )

    def get_expected_singlefile_output(self, archive):
        """Pigz restores the original filename for .gz files"""
        return "t.txt"
