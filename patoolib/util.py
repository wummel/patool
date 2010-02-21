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
import os
import sys
import subprocess
import mimetypes
import tempfile
import traceback

mimedb = mimetypes.MimeTypes(strict=False)
# add missing encodings for Python <=2.5
mimedb.encodings_map['.bz2'] = 'bzip2'
mimedb.suffix_map['.tbz2'] = '.tar.bz2'
mimedb.add_type('application/x-lzop', '.lzo', strict=False)
mimedb.add_type('application/x-arj', '.arj', strict=False)


class PatoolError (StandardError):
    """Raised when errors occur."""
    pass


def backtick (cmd):
    """Return output from command."""
    return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]


def run (cmd, **kwargs):
    """Run command and raise subprocess.CalledProcessError on error."""
    subprocess.check_call(cmd, **kwargs)


def guess_mime (filename):
    """Guess the MIME type of given filename. Uses first mimetypes
    and then file(1) as fallback."""
    mime, encoding = mimedb.guess_type(filename, strict=False)
    if mime is None and os.path.isfile(filename):
        cmd = ["file", "--brief", "--mime-type", filename]
        try:
            mime = backtick(cmd).strip()
        except OSError, msg:
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
    print >> out, "patool error:", msg


def log_internal_error (out=sys.stderr):
    print >> out, "patool: internal error"
    etype, value = sys.exc_info()[:2]
    traceback.print_exc()
    print >> out, "System info:"
    print >> out, "Python %s on %s" % (sys.version, sys.platform)
