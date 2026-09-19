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
"""Test that extracting a TAR or ZIP archive cannot write outside of the
requested output directory via '..' path components or absolute paths in
member names (aka "Zip Slip" / path traversal).
"""

import io
import os
import tarfile
import unittest
import zipfile

import patoolib
from patoolib import fileutil, util
from . import basedir


def _make_malicious_tar(archive: str, member_name: str) -> None:
    """Create a TAR archive with a single member using the given (potentially
    unsafe) name, bypassing tarfile.add()'s own filesystem-based naming.
    """
    with tarfile.open(archive, "w") as tfile:
        data = b"pwned"
        tarinfo = tarfile.TarInfo(name=member_name)
        tarinfo.size = len(data)
        tfile.addfile(tarinfo, io.BytesIO(data))


def _make_malicious_zip(archive: str, member_name: str) -> None:
    """Create a ZIP archive with a single member using the given (potentially
    unsafe) name.
    """
    with zipfile.ZipFile(archive, "w") as zfile:
        zfile.writestr(member_name, "pwned")


class ExtractSecurityTest(unittest.TestCase):
    """Test class for archive extraction path traversal safety."""

    def setUp(self):
        """Create a fresh temporary output directory for each test."""
        self.tmpdir = fileutil.tmpdir(dir=basedir)
        self.outdir = os.path.join(self.tmpdir, "out")
        os.makedirs(self.outdir)

    def tearDown(self):
        """Remove the temporary directory tree created in setUp()."""
        fileutil.rmtree(self.tmpdir)

    def _assert_extraction_refused(self, archive: str):
        """Assert that extracting archive raises PatoolError and writes nothing outside outdir."""
        with self.assertRaises(util.PatoolError):
            patoolib.extract_archive(archive, outdir=self.outdir, verbosity=-1)
        # Nothing should have been written outside of outdir.
        escaped = os.path.join(self.tmpdir, "evil.txt")
        self.assertFalse(os.path.exists(escaped))

    def test_tar_relative_path_traversal_is_refused(self):
        """A TAR member named with '..' components must not escape outdir."""
        archive = os.path.join(self.tmpdir, "evil.tar")
        _make_malicious_tar(archive, "../../evil.txt")
        self._assert_extraction_refused(archive)

    def test_tar_absolute_path_is_refused(self):
        """A TAR member with an absolute path must not escape outdir."""
        archive = os.path.join(self.tmpdir, "evil_abs.tar")
        _make_malicious_tar(archive, os.path.join(self.tmpdir, "evil.txt"))
        self._assert_extraction_refused(archive)

    def test_zip_relative_path_traversal_is_refused(self):
        """A ZIP member named with '..' components must not escape outdir."""
        archive = os.path.join(self.tmpdir, "evil.zip")
        _make_malicious_zip(archive, "../../evil.txt")
        self._assert_extraction_refused(archive)

    def test_zip_absolute_path_is_refused(self):
        """A ZIP member with an absolute path must not escape outdir."""
        archive = os.path.join(self.tmpdir, "evil_abs.zip")
        _make_malicious_zip(archive, os.path.join(self.tmpdir, "evil.txt"))
        self._assert_extraction_refused(archive)

    def test_safe_tar_still_extracts(self):
        """A normal TAR archive with only safe member names must still extract."""
        archive = os.path.join(self.tmpdir, "safe.tar")
        _make_malicious_tar(archive, "safe.txt")
        patoolib.extract_archive(archive, outdir=self.outdir, verbosity=-1)
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "safe.txt")))

    def test_safe_zip_still_extracts(self):
        """A normal ZIP archive with only safe member names must still extract."""
        archive = os.path.join(self.tmpdir, "safe.zip")
        _make_malicious_zip(archive, "safe.txt")
        patoolib.extract_archive(archive, outdir=self.outdir, verbosity=-1)
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "safe.txt")))


class UnsafeArchiveMemberUnitTest(unittest.TestCase):
    """Unit tests for util.get_unsafe_archive_member(), independent of any
    particular extraction backend.
    """

    def setUp(self):
        """Create a fresh temporary output directory for each test."""
        self.tmpdir = fileutil.tmpdir(dir=basedir)
        self.outdir = os.path.join(self.tmpdir, "out")
        os.makedirs(self.outdir)

    def tearDown(self):
        """Remove the temporary directory tree created in setUp()."""
        fileutil.rmtree(self.tmpdir)

    def test_tar_traversal_detected(self):
        """A TAR member with '..' components is reported as unsafe."""
        archive = os.path.join(self.tmpdir, "evil.tar")
        _make_malicious_tar(archive, "../escape.txt")
        unsafe = util.get_unsafe_archive_member("tar", archive, self.outdir)
        self.assertEqual(unsafe, "../escape.txt")

    def test_zip_traversal_detected(self):
        """A ZIP member with '..' components is reported as unsafe."""
        archive = os.path.join(self.tmpdir, "evil.zip")
        _make_malicious_zip(archive, "../escape.txt")
        unsafe = util.get_unsafe_archive_member("zip", archive, self.outdir)
        self.assertEqual(unsafe, "../escape.txt")

    def test_tar_safe_members_pass(self):
        """A TAR member with a normal relative path is not reported as unsafe."""
        archive = os.path.join(self.tmpdir, "safe.tar")
        _make_malicious_tar(archive, "dir/safe.txt")
        unsafe = util.get_unsafe_archive_member("tar", archive, self.outdir)
        self.assertIsNone(unsafe)

    def test_zip_safe_members_pass(self):
        """A ZIP member with a normal relative path is not reported as unsafe."""
        archive = os.path.join(self.tmpdir, "safe.zip")
        _make_malicious_zip(archive, "dir/safe.txt")
        unsafe = util.get_unsafe_archive_member("zip", archive, self.outdir)
        self.assertIsNone(unsafe)

    def test_unchecked_format_returns_none(self):
        """Formats other than tar/zip are not inspected by this function."""
        archive = os.path.join(self.tmpdir, "whatever.7z")
        with open(archive, "wb") as f:
            f.write(b"not a real archive")
        unsafe = util.get_unsafe_archive_member("7z", archive, self.outdir)
        self.assertIsNone(unsafe)
