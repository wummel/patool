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

# All text files have '42' as content.
TextFileContent = '42'

class ContentSet:
    """The test archives have one of several set of content files.
    The different content file sets have each a constant defined
    by this class.
    """

    # Recursive archives for extraction have a text file in a directory:
    # t/t.txt
    # Recursive archives for creation have two text files in directories:
    # foo dir/t.txt
    # foo dir/bar/t.txt
    Recursive = 'recursive'

    # Singlefile archives for extraction have a text file t.txt
    # Recursive archives for creation have a text file `foo .txt'
    Singlefile = 'singlefile'


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
        if kwargs.get('singlefile'):
            contents_default = ContentSet.Singlefile
        else:
            contents_default = ContentSet.Recursive
        contents = kwargs.get('contents', contents_default)
        self.archive_extract(filename, contents=contents)
        self.archive_create(filename, **kwargs)

    def archive_extract (self, filename, contents=ContentSet.Recursive):
        """Test archive extraction."""
        archive = os.path.join(datadir, filename)
        self.assertTrue(os.path.isabs(archive), "archive path is not absolute: %r" % archive)
        self._archive_extract(archive, contents)
        # archive name relative to tmpdir
        relarchive = os.path.join("..", archive[len(basedir)+1:])
        self._archive_extract(relarchive, contents, verbose=True)

    def _archive_extract (self, archive, contents, verbose=False):
        # create a temporary directory for extraction
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        try:
            olddir = os.getcwd()
        except OSError:
            olddir = None
        os.chdir(tmpdir)
        try:
            output = patoolib._handle_archive(archive, 'extract', program=self.program, verbose=verbose)
            self.check_extracted_contents(archive, output, contents)
        finally:
            if olddir:
                os.chdir(olddir)
            shutil.rmtree(tmpdir)

    def check_extracted_contents (self, archive, output, contents):
        if contents == ContentSet.Recursive:
            # outdir is the 't' directory of the archive
            self.assertEqual(output, 't')
            self.check_directory(output, 't')
            txtfile = os.path.join(output, 't.txt')
            self.check_textfile(txtfile, 't.txt')
        elif contents == ContentSet.Singlefile:
            txtfile = output
            self.check_textfile(txtfile, 't.txt')

    def check_directory (self, dirname, expectedname):
        self.assertTrue(os.path.isdir(dirname), dirname)
        self.assertEqual(os.path.basename(dirname), expectedname)

    def check_textfile (self, filename, expectedname):
        self.assertTrue(os.path.isfile(filename), filename)
        self.assertEqual(os.path.basename(filename), expectedname)
        self.assertEqual(get_filecontent(filename), TextFileContent)

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

    def archive_create (self, archive, srcfile=None, singlefile=False,
            format=None, compression=None, contents=None):
        """Test archive creation."""
        # determine filename which is added to the archive
        if srcfile is None:
            if singlefile:
                srcfile = 'foo .txt'
                contents = ContentSet.Singlefile
            else:
                srcfile = 'foo dir'
                contents = ContentSet.Recursive
        srcfile = os.path.join(datadir, srcfile)
        # The format and compression arguments are needed for creating
        # archives with unusual file extensions.
        kwargs = dict(
            program=self.program,
            format=format,
            compression=compression,
        )
        self._archive_create(archive, srcfile, kwargs)
        # create again in verbose mode
        kwargs['verbose'] = True
        self._archive_create(archive, srcfile, kwargs)
        # XXX check content

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
            if self.program in ('compress', 'py_gzip'):
                program = 'gzip'
            elif self.program == 'py_bz2':
                program = 'bzip2'
            elif self.program == 'zip':
                program = 'unzip'
            elif self.program in ('rzip', 'shorten'):
                program = 'py_echo'
                command = 'list'
            elif self.program == 'lcab':
                program = 'cabextract'
            patoolib._handle_archive(archive, command, program=program)
        finally:
            os.chdir(basedir)
            shutil.rmtree(tmpdir)


def get_filecontent(filename):
    fo = open(filename)
    try:
        return fo.read()
    finally:
        fo.close()


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
    if patoolib.program_supports_compression(program, codec):
        return True
    return patoolib.util.find_program(codec)
