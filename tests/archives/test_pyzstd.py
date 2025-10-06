# Copyright (C) 2025 Bastian Kleineidam
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
"""Test the python zstd module"""

from . import ArchiveTest, Content
from .. import needs_program, needs_module


class TestPyzstd(ArchiveTest):
    """Test class for the python zstd module"""

    program = 'py_zstd'

    @needs_module('compression.zstd')
    @needs_program('zstd')
    def test_py_zstd(self):
        """Extract and create ZSTD archives."""
        self.archive_extract('t.txt.zst', check=Content.Singlefile)
        self.archive_create('t.txt.zst', check=Content.Singlefile)

    @needs_program('file')
    @needs_program('zstd')
    @needs_module('compression.zstd')
    def test_py_zstd_file(self):
        """Extract renamed ZSTD archives."""
        self.archive_extract('t.txt.zst.foo', check=Content.Singlefile)
