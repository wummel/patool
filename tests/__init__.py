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

    def __init__ (self, *args):
        super(ArchiveTest, self).__init__(*args)
        # set program to use for archive handling
        self.program = None

    def archive_commands (self, filename, singlefile=False):
        self.archive_list(filename)
        self.archive_test(filename)
        self.archive_extract(filename)
        self.archive_create(filename, singlefile=singlefile)

    def archive_extract (self, filename):
        archive = os.path.join(datadir, filename)
        # create a temporary directory for extraction
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        os.chdir(tmpdir)
        try:
            patoolib._handle_archive(archive, 'extract', program=self.program)
            patoolib._handle_archive(archive, 'extract', program=self.program, force=True)
        finally:
            os.chdir(basedir)
            shutil.rmtree(tmpdir)

    def archive_list (self, filename):
        archive = os.path.join(datadir, filename)
        patoolib._handle_archive(archive, 'list', program=self.program)
        patoolib._handle_archive(archive, 'list', program=self.program, verbose=True)

    def archive_test (self, filename):
        archive = os.path.join(datadir, filename)
        patoolib._handle_archive(archive, 'test', program=self.program)
        patoolib._handle_archive(archive, 'test', program=self.program, verbose=True)

    def archive_create (self, filename, singlefile=False):
        # the file or directory to pack
        if singlefile:
            topack = os.path.join(datadir, 'foo.txt')
        else:
            topack = os.path.join(datadir, 'foo')
        # create a temporary directory for creation
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        archive = os.path.join(tmpdir, filename)
        os.chdir(tmpdir)
        try:
            patoolib._handle_archive(archive, 'create', topack, program=self.program)
            # not all programs can test what they create
            if self.program == 'compress':
                program = 'gzip'
            else:
                program = self.program
            patoolib._handle_archive(archive, 'test', program=program)
        finally:
            os.chdir(basedir)
            shutil.rmtree(tmpdir)


def needs_program (program):
    """Decorator skipping test if given program is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not find_executable(program):
                raise nose.SkipTest("program `%s' not available" % program)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_codec (program, codec):
    """Decorator skipping test if given program codec is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not find_executable(program):
                raise nose.SkipTest("program `%s' not available" % program)
            if not find_codec(program, codec):
                raise nose.SkipTest("codec `%s' for program `%s' not available" % (codec, program))
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def find_codec (program, codec):
    if program == '7z' and codec == 'rar':
        return patoolib.p7zip_supports_rar()
    return patoolib.find_encoding_program(program, codec)
