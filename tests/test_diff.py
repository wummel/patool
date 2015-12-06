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
from patoolib.util import run_checked
from . import datadir, needs_program, patool_cmd

class ArchiveDiffTest (unittest.TestCase):

    @needs_program('diff')
    @needs_program('tar')
    @needs_program('unzip')
    def test_diff (self):
        archive1 = os.path.join(datadir, "t.tar")
        archive2 = os.path.join(datadir, "t.zip")
        run_checked([sys.executable, patool_cmd, "-vv", "--non-interactive", "diff", archive1, archive2])
