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
import shutil
import patoolib
from .. import basedir, datadir

# All text files have '42' as content.
TextFileContent = '42'

class Content:
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
    # Singlefile archives for creation have a text file `foo .txt'
    Singlefile = 'singlefile'

    # Multifile archives for extraction have two text files: t.txt and t2.txt
    # Multifile archives for creation have two text files: foo .txt and foo2 .txt
    Multifile = 'multifile'


class ArchiveTest (unittest.TestCase):
    """Helper class for archive tests, handling one commandline program."""

    # set program to use for archive handling in subclass
    program = None

    def archive_commands (self, filename, **kwargs):
        """Run archive commands list, test, extract and create.
        All keyword arguments are delegated to the create test function."""
        self.archive_list(filename)
        if not kwargs.get('skip_test'):
            self.archive_test(filename)
        self.archive_extract(filename, check=kwargs.get('check', Content.Recursive))
        if not kwargs.get('skip_create'):
            self.archive_create(filename, **kwargs)

    def archive_extract (self, filename, check=Content.Recursive):
        """Test archive extraction."""
        archive = os.path.join(datadir, filename)
        self.assertTrue(os.path.isabs(archive), "archive path is not absolute: %r" % archive)
        self._archive_extract(archive, check)
        # archive name relative to tmpdir
        relarchive = os.path.join("..", archive[len(basedir)+1:])
        self._archive_extract(relarchive, check, verbosity=1)

    def _archive_extract (self, archive, check, verbosity=0):
        # create a temporary directory for extraction
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        try:
            olddir = patoolib.util.chdir(tmpdir)
            try:
                output = patoolib.extract_archive(archive, program=self.program, verbosity=verbosity, interactive=False)
                if check:
                    self.check_extracted_archive(archive, output, check)
            finally:
                if olddir:
                    os.chdir(olddir)
        finally:
            shutil.rmtree(tmpdir)

    def check_extracted_archive (self, archive, output, check):
        if check == Content.Recursive:
            # outdir is the 't' directory of the archive
            self.assertEqual(output, 't')
            self.check_directory(output, 't')
            txtfile = os.path.join(output, 't.txt')
            self.check_textfile(txtfile, 't.txt')
        elif check == Content.Singlefile:
            # a non-existing directory to ensure files do not exist in it
            ned = get_nonexisting_directory(os.getcwd())
            expected_output = os.path.basename(patoolib.util.get_single_outfile(ned, archive))
            self.check_textfile(output, expected_output)
        elif check == Content.Multifile:
            txtfile = os.path.join(output, 't.txt')
            self.check_textfile(txtfile, 't.txt')
            txtfile2 = os.path.join(output, 't2.txt')
            self.check_textfile(txtfile2, 't2.txt')

    def check_directory (self, dirname, expectedname):
        """Check that directory exists."""
        self.assertTrue(os.path.isdir(dirname), dirname)
        self.assertEqual(os.path.basename(dirname), expectedname)

    def check_textfile (self, filename, expectedname):
        """Check that filename exists and has the default content."""
        self.assertTrue(os.path.isfile(filename), repr(filename))
        self.assertEqual(os.path.basename(filename), expectedname)
        self.assertEqual(get_filecontent(filename), TextFileContent)

    def archive_list (self, filename):
        """Test archive listing."""
        archive = os.path.join(datadir, filename)
        for verbosity in (-1, 0, 1, 2):
            patoolib.list_archive(archive, program=self.program, verbosity=verbosity, interactive=False)

    def archive_test (self, filename):
        """Test archive testing."""
        archive = os.path.join(datadir, filename)
        for verbosity in (-1, 0, 1, 2):
            patoolib.test_archive(archive, program=self.program, verbosity=verbosity, interactive=False)

    def archive_create (self, archive, srcfiles=None, check=Content.Recursive):
        """Test archive creation."""
        if srcfiles is None:
            if check == Content.Recursive:
                srcfiles = ('t',)
            elif check == Content.Singlefile:
                srcfiles = ('t.txt',)
            elif check == Content.Multifile:
                srcfiles = ('t.txt', 't2.txt',)
            else:
                raise ValueError('invalid check value %r' % check)
        olddir = patoolib.util.chdir(datadir)
        try:
            # The format and compression arguments are needed for creating
            # archives with unusual file extensions.
            for verbosity in (-1, 0, 1, 2):
                self._archive_create(archive, srcfiles, program=self.program, verbosity=verbosity)
        finally:
            if olddir:
                os.chdir(olddir)

    def _archive_create (self, archive, srcfiles, program=None, verbosity=0):
        """Create archive from filename."""
        for srcfile in srcfiles:
            self.assertFalse(os.path.isabs(srcfile))
            self.assertTrue(os.path.exists(srcfile))
        # create a temporary directory for creation
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        try:
            archive = os.path.join(tmpdir, archive)
            self.assertTrue(os.path.isabs(archive), "archive path is not absolute: %r" % archive)
            patoolib.create_archive(archive, srcfiles, verbosity=verbosity, interactive=False, program=program)
            self.assertTrue(os.path.isfile(archive))
            self.check_created_archive_with_test(archive)
            self.check_created_archive_with_diff(archive, srcfiles)
        finally:
            shutil.rmtree(tmpdir)

    def check_created_archive_with_test(self, archive):
        command = patoolib.test_archive
        program = self.program
        # special case for programs that cannot test what they create
        if self.program in ('compress', 'py_gzip'):
            program = 'gzip'
        elif self.program == 'py_bz2':
            program = 'bzip2'
        elif self.program == 'py_lzma':
            program = 'xz'
        elif self.program == 'zip':
            program = 'unzip'
        elif self.program in ('rzip', 'shorten'):
            program = 'py_echo'
            command = patoolib.list_archive
        elif self.program == 'lcab':
            program = 'cabextract'
        elif self.program == 'genisoimage':
            program = '7z'
        elif self.program == 'shar':
            return
        command(archive, program=program)

    def check_created_archive_with_diff(self, archive, srcfiles):
        """Extract created archive again and compare the contents."""
        # diff srcfile and output
        diff = patoolib.util.find_program("diff")
        if not diff:
            return
        program = self.program
        # special case for programs that cannot extract what they create
        if self.program == 'compress':
            program = 'gzip'
        elif self.program == 'zip':
            program = 'unzip'
        elif self.program == 'lcab':
            program = 'cabextract'
        elif self.program == 'shar':
            program = 'unshar'
        elif self.program == 'genisoimage':
            program = '7z'
        tmpdir = patoolib.util.tmpdir(dir=basedir)
        try:
            olddir = patoolib.util.chdir(tmpdir)
            try:
                output = patoolib.extract_archive(archive, program=program, interactive=False)
                if len(srcfiles) == 1:
                    source = os.path.join(datadir, srcfiles[0])
                    patoolib.util.run_checked([diff, "-urN", source, output])
                else:
                    for srcfile in srcfiles:
                        source = os.path.join(datadir, srcfile)
                        target = os.path.join(output, srcfile)
                        patoolib.util.run_checked([diff, "-urN", source, target])
            finally:
                if olddir:
                    os.chdir(olddir)
        finally:
            shutil.rmtree(tmpdir)


def get_filecontent(filename):
    """Get file data as text."""
    with open(filename) as fo:
        return fo.read()


def get_nonexisting_directory(basedir):
    """Note: this is _not_ intended to be used to create a directory."""
    d = os.path.join(basedir, "foo")
    while os.path.exists(d):
        d += 'a'
        if len(d) > 100:
            # wtf
            raise ValueError('could not construct unique directory name at %r' % basedir)
    return d
