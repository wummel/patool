# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Bastian Kleineidam
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

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')

class ArchiveTest (unittest.TestCase):
    """Helper class for achive tests."""

    def __init__ (self, *args):
        """Initialize this archive test."""
        super(ArchiveTest, self).__init__(*args)
        # set program to use for archive handling
        self.program = None

    def archive_commands (self, filename, **kwargs):
        """Run archive commands list, test, extract and create.
        All keyword arguments are delegated to the create test function."""
        self.archive_list(filename)
        self.archive_test(filename)
        self.archive_extract(filename)
        self.archive_create(filename, **kwargs)

    def archive_extract (self, filename):
        """Test archive extraction."""
        archive = os.path.join(datadir, filename)
        # create a temporary directory for extraction
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        try:
            olddir = os.getcwd()
        except OSError:
            olddir = None
        os.chdir(tmpdir)
        # archive name relative to tmpdir
        relarchive = os.path.join("..", archive[len(basedir)+1:])
        try:
            patoolib._handle_archive(archive, 'extract', program=self.program)
            patoolib._handle_archive(relarchive, 'extract', program=self.program, verbose=True)
        finally:
            if olddir:
                os.chdir(olddir)
            shutil.rmtree(tmpdir)

    def archive_list (self, filename):
        """Test archive listing."""
        archive = os.path.join(datadir, filename)
        patoolib._handle_archive(archive, 'list', program=self.program)
        patoolib._handle_archive(archive, 'list', program=self.program, verbose=True)

    def archive_test (self, filename):
        """Test archive testing."""
        archive = os.path.join(datadir, filename)
        patoolib._handle_archive(archive, 'test', program=self.program)
        patoolib._handle_archive(archive, 'test', program=self.program, verbose=True)

    def archive_create (self, filename, singlefile=False, format=None, encoding=None):
        """Test archive creation."""
        # the file or directory to pack (note that they have spaces)
        if singlefile:
            topack = os.path.join(datadir, 'foo .txt')
        else:
            topack = os.path.join(datadir, 'foo dir')
        # The format and encoding arguments are needed for creating
        # archives with unusual file extensions.
        kwargs = dict(
            program=self.program,
            format=format,
            encoding=encoding,
        )
        self._archive_create(filename, topack, kwargs)
        kwargs['verbose'] = True
        self._archive_create(filename, topack, kwargs)

    def _archive_create (self, filename, topack, kwargs):
        """Create archive from filename."""
        # create a temporary directory for creation
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        archive = os.path.join(tmpdir, filename)
        os.chdir(tmpdir)
        try:
            patoolib._handle_archive(archive, 'create', topack, **kwargs)
            self.assertTrue(os.path.isfile(archive))
            # test the created archive
            command = 'test'
            program = self.program
            # special case for programs that cannot test what they create
            if self.program in ('compress', 'pygzip'):
                program = 'gzip'
            elif self.program == 'pybz2':
                program = 'bzip2'
            elif self.program == 'zip':
                program = 'unzip'
            elif self.program == 'rzip':
                program = 'echo'
                command = 'list'
            patoolib._handle_archive(archive, command, program=program)
        finally:
            os.chdir(basedir)
            shutil.rmtree(tmpdir)


def needs_os (name):
    """Decorator skipping test if given program is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if os.name != name:
                raise nose.SkipTest("operating system %s not found" % name)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_program (program):
    """Decorator skipping test if given program is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not patoolib.util.find_program(program):
                raise nose.SkipTest("program `%s' not available" % program)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_one_program (programs):
    """Decorator skipping test if not one of given programs are available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            for program in programs:
                if patoolib.util.find_program(program):
                    break
            else:
                raise nose.SkipTest("None of programs %s available" % programs)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_codec (program, codec):
    """Decorator skipping test if given program codec is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not patoolib.util.find_program(program):
                raise nose.SkipTest("program `%s' not available" % program)
            if not has_codec(program, codec):
                raise nose.SkipTest("codec `%s' for program `%s' not available" % (codec, program))
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def has_codec (program, codec):
    """Test if program supports given codec."""
    if program == '7z' and codec == 'rar':
        return patoolib.util.p7zip_supports_rar()
    return patoolib.find_encoding_program(program, codec)
