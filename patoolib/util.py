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
from distutils.spawn import find_executable

mimedb = mimetypes.MimeTypes(strict=False)
# add missing encodings and mimetypes
mimedb.encodings_map['.bz2'] = 'bzip2'
mimedb.encodings_map['.lzma'] = 'lzma'
mimedb.encodings_map['.xz'] = 'xz'
mimedb.encodings_map['.lz'] = 'lzip'
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
mimedb.add_type('application/x-ace', '.ace', strict=False)
# Since .a is already a common type, strict=True must be used.
mimedb.add_type('application/x-archive', '.a', strict=True)
mimedb.add_type('application/x-alzip', '.alz', strict=False)
mimedb.add_type('application/x-arc', '.arc', strict=False)


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
    """Run command and raise PatoolError on error."""
    retcode = subprocess.call(cmd, **kwargs)
    if retcode:
        msg = "Command `%s' returned non-zero exit status %d" % (cmd, retcode)
        raise PatoolError(msg)
    return retcode


@memoized
def guess_mime (filename):
    """Guess the MIME type of given filename using file(1) and if that
    fails by looking at the filename extension with the Python mimetypes
    module.

    The result of this function is cached.
    """
    mime, encoding = guess_mime_file(filename)
    if mime is None:
        mime, encoding = guess_mime_mimedb(filename)
    assert mime is not None or encoding is None
    return mime, encoding


Encoding2Mime = {
    'gzip': "application/x-gzip",
    'bzip2': "application/x-bzip2",
    'compress': "application/x-compress",
    'lzma': "application/x-lzma",
    'lzip': "application/x-lzip",
    'xz': "application/x-xz",
}
Mime2Encoding = dict([(value, key) for key, value in Encoding2Mime.items()])


def guess_mime_mimedb (filename):
    """Guess MIME type from given filename."""
    mime, encoding = mimedb.guess_type(filename, strict=False)
    from patoolib import ArchiveMimetypes, ArchiveEncodings
    if mime not in ArchiveMimetypes and encoding in ArchiveEncodings:
        # Files like 't.txt.gz' are recognized with encoding as format, and
        # an unsupported mime-type like 'text/plain'. Fix this.
        mime = Encoding2Mime[encoding]
        encoding = None
    return mime, encoding


def guess_mime_file (filename):
    """Determine MIME type of filename with file(1):
     (a) using file(1) --mime
     (b) using file(1) and look the result string
    """
    mime, encoding = None, None
    if os.path.isfile(filename):
        file_prog = find_program("file")
        if file_prog:
            mime, encoding = guess_mime_file_mime(file_prog, filename)
            if mime is None:
                mime = guess_mime_file_text(file_prog, filename)
    return mime, encoding


def guess_mime_file_mime (file_prog, filename):
    """Determine MIME type of filename with file(1) and --mime option."""
    mime, encoding = None, None
    cmd = [file_prog, "--brief", "--mime-type", filename]
    try:
        mime = backtick(cmd).strip()
    except OSError, msg:
        # ignore errors, as file(1) is only a fallback
        return mime, encoding
    from patoolib import ArchiveMimetypes
    if mime in Encoding2Mime.values():
        # try to look inside compressed archives
        cmd = [file_prog, "--brief", "--mime", "--uncompress", filename]
        try:
            outparts = backtick(cmd).strip().split(";")
        except OSError, msg:
            # ignore errors, as file(1) is only a fallback
            return mime, encoding
        mime2 = outparts[0]
        if mime2 in ArchiveMimetypes:
            mime = mime2
            encoding = get_file_mime_encoding(outparts)
    if mime not in ArchiveMimetypes:
        mime, encoding = None, None
    return mime, encoding


def get_file_mime_encoding (parts):
    """Get encoding value from splitted output of file --mime --uncompress."""
    for part in parts:
        for subpart in part.split(" "):
            if subpart.startswith("compressed-encoding="):
                mime = subpart.split("=")[1].strip()
                return Mime2Encoding.get(mime)
    return None


# Match file(1) output text to mime types
FileText2Mime = {
    "7-zip archive data": "application/x-7z-compressed",
    "ACE archive data": "application/x-ace",
    "ARJ archive data": "application/x-arj",
    "bzip2 compressed data": "application/x-bzip2",
    "cpio archive": "application/x-cpio",
    "Debian binary package": "application/x-debian-package",
    "gzip compressed data": "application/x-gzip",
    "lzop compressed data": "application/x-lzop",
    "Microsoft Cabinet archive data": "application/vnd.ms-cab-compressed",
    "RAR archive data": "application/x-rar",
    "RPM ": "application/x-redhat-package-manager",
    "POSIX tar archive": "application/x-tar",
    "xz compressed data": "application/x-xz",
    "Zip archive data": "application/zip",
    "compress'd data": "application/x-compress",
    "lzip compressed data": "application/x-lzip",
    "current ar archive": "application/x-archive",
    "LHa ": "application/x-lha",
    "ARC archive data": "application/x-arc",
}

def guess_mime_file_text (file_prog, filename):
    """Determine MIME type of filename with file(1)."""
    cmd = [file_prog, "--brief", filename]
    try:
        output = backtick(cmd).strip()
    except OSError, msg:
        # ignore errors, as file(1) is only a fallback
        return None
    # match output against known strings
    for matcher, mime in FileText2Mime.items():
        if output.startswith(matcher):
            return mime
    return None


def check_filename (filename):
    """Ensure that given filename is a valid, existing file."""
    if not os.path.isfile(filename):
        raise PatoolError("`%s' is not a file." % filename)
    if not os.path.exists(filename):
        raise PatoolError("File `%s' not found." % filename)
    if not os.access(filename, os.R_OK):
        raise PatoolError("File `%s' not readable." % filename)


def set_mode (filename, flags):
    """Set mode flags for given filename if not already set."""
    try:
        mode = os.lstat(filename).st_mode
    except OSError:
        # ignore
        return
    if not (mode & flags):
        try:
            os.chmod(filename, flags | mode)
        except OSError, msg:
            log_error("could not set mode flags for `%s': %s" % (filename, msg))


def tmpdir (dir=None):
    """Return a temporary directory for extraction."""
    return tempfile.mkdtemp(suffix='', prefix='Unpack_', dir=dir)


def tmpfile (dir=None, prefix="temp", suffix=None):
    """Return a temporary file."""
    return tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)[1]


def shell_quote (value):
    """Quote all shell metacharacters in given string value."""
    return '%s' % value


def stripext (filename):
    """Return the basename without extension of given filename."""
    return os.path.splitext(os.path.basename(filename))[0]


def get_single_outfile (directory, archive):
    """Get output filename if archive is in a single file format like gzip."""
    outfile = os.path.join(directory, stripext(archive))
    if archive == outfile:
        # prevent overwriting the archive itself
        outfile += ".raw"
    return outfile


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
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip")
        try:
            return _winreg.QueryValueEx(key, "Path")[0]
        finally:
            _winreg.CloseKey(key)
    except WindowsError:
        return ""


def strlist_with_or (list):
    """Return comma separated string, and last entry appended with ' or '."""
    if len(list) > 1:
        return "%s or %s" % (", ".join(list[:-1]), list[-1])
    return ", ".join(list)
