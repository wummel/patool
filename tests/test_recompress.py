# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Bastian Kleineidam
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
import unittest
import os
import sys
import shutil
from patoolib import util
from . import datadir, needs_one_program, patool_cmd

class ArchiveRecompressTest (unittest.TestCase):

    def recompress(self, name):
        """Recompress archive with given name."""
        archive = os.path.join(datadir, name)
        ext = os.path.splitext(archive)[1]
        tmpfile = util.tmpfile(suffix=ext)
        try:
            shutil.copy(archive, tmpfile)
            util.run_checked([sys.executable, patool_cmd, "-vv", "--non-interactive", "recompress", tmpfile])
        finally:
            if os.path.exists(tmpfile):
                os.remove(tmpfile)

    @needs_one_program(('zip', '7z'))
    def test_repack (self):
        self.recompress('t.zip')

