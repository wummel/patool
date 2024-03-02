# Copyright (C) 2010-2024 Bastian Kleineidam
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
"""MIME type detection functions."""
import os
import mimetypes
import subprocess
from . import ArchiveMimetypes, ArchiveCompressions, program_supports_compression
from .log import log_error, log_warning
from .util import memoized, find_program, backtick


# internal MIME database
mimedb = None


def init_mimedb():
    """Initialize the internal MIME database."""
    global mimedb
    try:
        mimedb = mimetypes.MimeTypes(strict=False)
    except Exception as msg:
        log_error(f"could not initialize MIME database: {msg}")
        return
    add_mimedb_data(mimedb)


def add_mimedb_data(mimedb):
    """Add missing encodings and mimetypes to MIME database."""
    mimedb.encodings_map[".bz2"] = "bzip2"
    mimedb.encodings_map[".lzma"] = "lzma"
    mimedb.encodings_map[".xz"] = "xz"
    mimedb.encodings_map[".lz"] = "lzip"
    mimedb.encodings_map[".zst"] = "zstd"
    mimedb.suffix_map[".tbz2"] = ".tar.bz2"
    add_mimetype(mimedb, "application/x-lzop", ".lzo")
    add_mimetype(mimedb, "application/x-adf", ".adf")
    add_mimetype(mimedb, "application/x-arj", ".arj")
    add_mimetype(mimedb, "application/x-bzip3", ".bz3")
    add_mimetype(mimedb, "application/x-lzma", ".lzma")
    add_mimetype(mimedb, "application/x-xz", ".xz")
    add_mimetype(mimedb, "application/java-archive", ".jar")
    add_mimetype(mimedb, "application/x-rar", ".rar")
    add_mimetype(mimedb, "application/x-rar", ".cbr")
    add_mimetype(mimedb, "application/x-7z-compressed", ".7z")
    add_mimetype(mimedb, "application/x-7z-compressed", ".cb7")
    add_mimetype(mimedb, "application/x-cab", ".cab")
    add_mimetype(mimedb, "application/x-rpm", ".rpm")
    add_mimetype(mimedb, "application/x-debian-package", ".deb")
    add_mimetype(mimedb, "application/x-ace", ".ace")
    add_mimetype(mimedb, "application/x-ace", ".cba")
    add_mimetype(mimedb, "application/x-archive", ".a")
    add_mimetype(mimedb, "application/x-alzip", ".alz")
    add_mimetype(mimedb, "application/x-arc", ".arc")
    add_mimetype(mimedb, "application/x-lrzip", ".lrz")
    add_mimetype(mimedb, "application/x-lha", ".lha")
    add_mimetype(mimedb, "application/x-lzh", ".lzh")
    add_mimetype(mimedb, "application/x-lz4", ".lz4")
    add_mimetype(mimedb, "application/x-rzip", ".rz")
    add_mimetype(mimedb, "application/x-zoo", ".zoo")
    add_mimetype(mimedb, "application/x-dms", ".dms")
    add_mimetype(mimedb, "application/x-zip-compressed", ".crx")
    add_mimetype(mimedb, "application/x-shar", ".shar")
    add_mimetype(mimedb, "application/x-tar", ".cbt")
    add_mimetype(mimedb, "application/x-vhd", ".vhd")
    add_mimetype(mimedb, "audio/x-ape", ".ape")
    add_mimetype(mimedb, "audio/x-shn", ".shn")
    add_mimetype(mimedb, "audio/flac", ".flac")
    add_mimetype(mimedb, "application/x-chm", ".chm")
    add_mimetype(mimedb, "application/x-iso9660-image", ".iso")
    add_mimetype(mimedb, "application/zip", ".cbz")
    add_mimetype(mimedb, "application/zip", ".epub")
    add_mimetype(mimedb, "application/zip", ".apk")
    add_mimetype(mimedb, "application/zpaq", ".zpaq")
    add_mimetype(mimedb, "application/zstd", ".zst")


def add_mimetype(mimedb, mimetype, extension):
    """Add or replace a mimetype to be used with the given extension."""
    # If extension is already a common type, strict=True must be used.
    strict = extension in mimedb.types_map[True]
    mimedb.add_type(mimetype, extension, strict=strict)


@memoized
def guess_mime(filename):
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
    "gzip": "application/gzip",
    "bzip2": "application/x-bzip2",
    "compress": "application/x-compress",
    "lzma": "application/x-lzma",
    "lzip": "application/x-lzip",
    "xz": "application/x-xz",
    "zstd": "application/zstd",
}
Mime2Encoding = dict([(_val, _key) for _key, _val in Encoding2Mime.items()])
# libmagic before version 5.14 identified .gz files as application/x-gzip
Mime2Encoding["application/x-gzip"] = "gzip"


def guess_mime_mimedb(filename):
    """Guess MIME type from given filename.
    @return: tuple (mime, encoding)
    """
    mime, encoding = None, None
    if mimedb is not None:
        mime, encoding = mimedb.guess_type(filename, strict=False)
    if mime not in ArchiveMimetypes and encoding in ArchiveCompressions:
        # Files like 't.txt.gz' are recognized with encoding as format, and
        # an unsupported mime-type like 'text/plain'. Fix this.
        mime = Encoding2Mime[encoding]
        encoding = None
    return mime, encoding


def guess_mime_file(filename):
    """Determine MIME type of filename with file(1):
     (a) using `file --brief --mime-type`
     (b) using `file --brief` and look at the result string
     (c) detect compressed archives (eg. .tar.gz) using
         `file --brief --mime --uncompress --no-sandbox`
    @return: tuple (mime, encoding)
    """
    mime, encoding = None, None
    base, ext = os.path.splitext(filename)
    if ext.lower() in (".alz",):
        # let mimedb recognize these extensions
        return mime, encoding
    if os.path.isfile(filename):
        file_prog = find_program("file")
        if file_prog:
            mime, encoding = guess_mime_file_mime(file_prog, filename)
            if mime is None:
                mime = guess_mime_file_text(file_prog, filename)
                encoding = None
    if mime in Mime2Encoding:
        # try to look inside compressed archives
        cmd = [file_prog, "--brief", "--mime", "--uncompress", "--no-sandbox", filename]
        try:
            outparts = backtick(cmd).strip().split(";")
            mime2 = outparts[0].split(" ", 1)[0]
        except (OSError, subprocess.CalledProcessError) as err:
            log_warning(f"error executing {cmd}: {err}")
            mime2 = None
        # Some file(1) implementations return an empty or unknown mime type
        # when the uncompressor program is not installed, other
        # implementation return the original file type.
        # The following detects both cases.
        if (
            mime2 in ("application/x-empty", "application/octet-stream")
            or mime2 in Mime2Encoding
            or not mime2
        ):
            # The uncompressor program file(1) uses is not installed
            # or is not able to uncompress.
            # Try to get mime information from the file extension.
            mime2, encoding2 = guess_mime_mimedb(filename)
            if mime2 in ArchiveMimetypes:
                mime = mime2
                encoding = encoding2
        elif mime2 in ArchiveMimetypes:
            mime = mime2
            encoding = get_file_mime_encoding(outparts)
    # Only return mime and encoding if the given mime can natively support the encoding.
    if program_supports_compression(ArchiveMimetypes.get(mime), encoding):
        return mime, encoding
    else:
        # If encoding is None, default back to `mime`.
        return Encoding2Mime.get(encoding, mime), None


def guess_mime_file_mime(file_prog, filename):
    """Determine MIME type of filename with file(1) and --mime option.
    @return: tuple (mime, encoding)
    """
    mime, encoding = None, None
    cmd = [file_prog, "--brief", "--mime-type", filename]
    try:
        mime = backtick(cmd).strip()
    except OSError as err:
        # ignore errors, as file(1) is only a fallback
        log_warning(f"error executing {cmd}: {err}")
    if mime not in ArchiveMimetypes:
        mime, encoding = None, None
    return mime, encoding


def get_file_mime_encoding(parts):
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
    "Amiga DOS disk": "application/x-adf",
    "ARJ archive data": "application/x-arj",
    "bzip2 compressed data": "application/x-bzip2",
    "bzip3 compressed data": "application/x-bzip3",
    "cpio archive": "application/x-cpio",
    "ASCII cpio archive": "application/x-cpio",
    "Debian binary package": "application/x-debian-package",
    "gzip compressed data": "application/x-gzip",
    "LZMA compressed data": "application/x-lzma",
    "LRZIP compressed data": "application/x-lrzip",
    "lzop compressed data": "application/x-lzop",
    "Microsoft Cabinet archive data": "application/vnd.ms-cab-compressed",
    "RAR archive data": "application/x-rar",
    "RPM ": "application/x-redhat-package-manager",
    "POSIX tar archive": "application/x-tar",
    "xz compressed data": "application/x-xz",
    "Zip archive data": "application/zip",
    "compress'd data": "application/x-compress",
    "lzip compressed data": "application/x-lzip",
    "rzip compressed data": "application/x-rzip",
    "current ar archive": "application/x-archive",
    "LHa ": "application/x-lha",
    "ARC archive data": "application/x-arc",
    "Zoo archive data": "application/x-zoo",
    "DMS archive data": "application/x-dms",
    "Monkey's Audio": "audio/x-ape",
    "FLAC audio bitstream data": "audio/flac",
    "MS Windows HtmlHelp Data": "application/x-chm",
    "ZPAQ stream": "application/zpaq",
}


def guess_mime_file_text(file_prog, filename):
    """Determine MIME type of filename with file(1)."""
    try:
        cmd = [file_prog, "--brief", filename]
        output = backtick(cmd).strip()
    except OSError as err:
        # ignore errors, as file(1) is only a fallback
        log_warning(f"error executing {cmd}: {err}")
        return None
    # match output against known strings
    for matcher, mime in FileText2Mime.items():
        if output.startswith(matcher) and mime in ArchiveMimetypes:
            return mime
    return None


init_mimedb()
