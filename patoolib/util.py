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
"""Utility functions."""
from __future__ import with_statement
import os
import sys
import subprocess
import mimetypes
import tempfile
import traceback
from distutils.spawn import find_executable

mimedb = mimetypes.MimeTypes(strict=False)
# add missing encodings and mimetypes
mimedb.encodings_map['.bz2'] = 'bzip2'
mimedb.encodings_map['.lzma'] = 'lzma'
mimedb.encodings_map['.xz'] = 'xz'
mimedb.suffix_map['.tbz2'] = '.tar.bz2'
mimedb.add_type('application/x-lzop', '.lzo', strict=False)
mimedb.add_type('application/x-arj', '.arj', strict=False)
mimedb.add_type('application/x-lzma', '.lzma', strict=False)
mimedb.add_type('application/x-xz', '.xz', strict=False)
mimedb.add_type('application/java-archive', '.jar', strict=False)
mimedb.add_type('application/x-rar', '.rar', strict=False)
mimedb.add_type('application/x-7z-compressed', '.7z', strict=False)
mimedb.add_type('application/x-cab', '.cab', strict=False)
mimedb.add_type('application/x-rpm', '.rpm', strict=False)
mimedb.add_type('application/x-debian-package', '.deb', strict=False)


class PatoolError (StandardError):
    """Raised when errors occur."""
    pass


class memoized (object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated."""

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


def backtick (cmd):
    """Return output from command."""
    return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]


def run (cmd, **kwargs):
    """Run command and raise subprocess.CalledProcessError on error."""
    subprocess.check_call(cmd, **kwargs)


@memoized
def guess_mime (filename):
    """Guess the MIME type of given filename. Uses first mimetypes
    and then file(1) as fallback."""
    mime, encoding = mimedb.guess_type(filename, strict=False)
    if mime is None and os.path.isfile(filename):
        file_prog = find_program("file")
        if file_prog:
            cmd = [file_prog, "--brief", "--mime-type", filename]
            try:
                mime = backtick(cmd).strip()
            except OSError, msg:
                # ignore errors, as file(1) is only a fallback
                pass
    return mime, encoding


def check_filename (filename):
    """Ensure that given filename is a valid, existing file."""
    if not os.path.isfile(filename):
        raise PatoolError("`%s' is not a file." % filename)
    if not os.path.exists(filename):
        raise PatoolError("File `%s' not found." % filename)
    if not os.access(filename, os.R_OK):
        raise PatoolError("File `%s' not readable." % filename)


def tmpdir (dir=None):
    """Return a temporary directory for extraction."""
    return tempfile.mkdtemp(suffix='', prefix='Unpack_', dir=dir)


def shell_quote (value):
    """Quote all shell metacharacters in given string value."""
    return '%s' % value


def stripext (filename):
    """Return the basename without extension of given filename."""
    return os.path.splitext(os.path.basename(filename))[0]


def log_error (msg, out=sys.stderr):
    """Print error message to stderr (or any other given output)."""
    print >> out, "patool error:", msg


def log_internal_error (out=sys.stderr):
    """Print internal error message to stderr."""
    print >> out, "patool: internal error"
    etype, value = sys.exc_info()[:2]
    traceback.print_exc()
    print >> out, "System info:"
    print >> out, "Python %s on %s" % (sys.version, sys.platform)


def p7zip_supports_rar ():
    """Determine if the RAR codec is installed for 7z program."""
    if os.name == 'nt':
        # Assume RAR support is compiled into the binary.
        return True
    return os.path.exists('/usr/lib/p7zip/Codecs/Rar29.so')


@memoized
def find_program (program):
    """Look for program in environment PATH variable."""
    path = os.environ['PATH']
    if os.name == 'nt':
        path = append_to_path(path, get_nt_7z_dir())
    return find_executable(program, path=path)


def append_to_path (path, directory):
    """Add a directory to the PATH env variable, if it is a valid directory."""
    if not os.path.isdir(directory) or directory in path:
        return path
    if not path.endswith(os.pathsep):
        path += os.pathsep
    return path + directory


def get_nt_7z_dir ():
    """Return 7-Zip directory from registry, or an empty string."""
    try:
        import _winreg
        with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip") as key:
            return _winreg.QueryValueEx(key, "Path")[0]
    except WindowsError:
        return ""


def strlist_with_or (list):
    """Return comma separated string, and last entry appended with ' or '."""
    if len(list) > 1:
        return "%s or %s" % (", ".join(list[:-1]), list[-1])
    return ", ".join(list)
