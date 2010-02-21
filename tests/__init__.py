# -*- coding: utf-8 -*-
# Copyright (C) 2010 Bastian Kleineidam
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
import shutil
import nose
import patoolib
from distutils.spawn import find_executable

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')

class ArchiveTest (unittest.TestCase):
    """Helper class for achive tests."""

    def archive_test (self, filename, cmd):
        self.archive_list(filename, cmd)
        self.archive_extract(filename, cmd)

    def archive_extract (self, filename, cmd):
        archive = os.path.join(datadir, filename)
        # create a temporary directory for extraction
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        os.chdir(tmpdir)
        try:
            patoolib._handle_archive(archive, 'extract', cmd=cmd)
            patoolib._handle_archive(archive, 'extract', cmd=cmd, force=True)
        finally:
            os.chdir(basedir)
            shutil.rmtree(tmpdir)

    def archive_list (self, filename, cmd):
        archive = os.path.join(datadir, filename)
        patoolib._handle_archive(archive, 'list', cmd=cmd)
        patoolib._handle_archive(archive, 'list', cmd=cmd, verbose=True)


def needs_cmd (cmd):
    """Decorator skipping test if given command is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not find_executable(cmd):
                raise nose.SkipTest("command `%s' not available" % cmd)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog
