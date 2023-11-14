# -*- coding: utf-8 -*-
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
import inspect
import sys
if not hasattr(sys, "version_info") or sys.version_info < (3, 10, 0, "final", 0):
    raise SystemExit("This program requires Python 3.10 or later.")
import os
import shutil
import importlib
# PEP 396
from .configuration import App, Version as __version__ # noqa: F401
from . import fileutil, log, util
__all__ = ['list_formats', 'list_archive', 'extract_archive', 'test_archive',
    'create_archive', 'diff_archives', 'search_archive', 'repack_archive',
    'is_archive', 'program_supports_compression']


# Supported archive commands
ArchiveCommands = ('list', 'extract', 'test', 'create')

# Supported archive formats
ArchiveFormats = (
    '7z', 'ace', 'adf', 'alzip', 'ape', 'ar', 'arc', 'arj',
    'bzip2', 'bzip3', 'cab', 'chm', 'compress', 'cpio', 'deb', 'dms',
    'flac', 'gzip', 'iso', 'lrzip', 'lz4', 'lzh', 'lzip', 'lzma', 'lzop',
    'rar', 'rpm', 'rzip', 'shar', 'shn', 'tar', 'vhd', 'xz',
    'zip', 'zoo', 'zpaq', 'zstd')

# Supported compressions (used with tar for example)
# Note that all compressions must also be archive formats
ArchiveCompressions = (
    'bzip2', 'compress', 'gzip', 'lzip', 'lzma', 'xz', 'zstd',
)

# Map MIME types to archive format
ArchiveMimetypes = {
    'application/gzip': 'gzip',
    'application/jar': 'zip',  # reported on older systems such as ubuntu 14.04
    'application/java-archive': 'zip',
    'application/vnd.android.package-archive': 'zip',
    'application/rar': 'rar',
    'application/vnd.ms-cab-compressed': 'cab',
    'application/x-7z-compressed': '7z',
    'application/x-ace': 'ace',
    'application/x-adf': 'adf',
    'application/x-alzip': 'alzip',
    'application/x-archive': 'ar',
    'application/x-arc': 'arc',
    'application/x-arj': 'arj',
    'application/x-bzip2': 'bzip2',
    'application/x-bzip3': 'bzip3',
    'application/x-cab': 'cab',
    'application/x-chm': 'chm',
    'application/x-compress': 'compress',
    'application/x-cpio': 'cpio',
    'application/x-debian-package': 'deb',
    'application/x-dms': 'dms',
    'application/x-gzip': 'gzip',
    'application/x-iso9660-image': 'iso',
    'application/x-lz4': 'lz4',
    'application/x-lzop': 'lzop',
    'application/x-lzma': 'lzma',
    'application/x-lzip': 'lzip',
    'application/x-lha': 'lzh',
    'application/x-lrzip': 'lrzip',
    'application/x-lzh': 'lzh',
    'application/x-rar': 'rar',
    'application/x-redhat-package-manager': 'rpm',
    'application/x-rpm': 'rpm',
    'application/x-rzip': 'rzip',
    'application/x-shar': 'shar',
    'application/x-tar': 'tar',
    'application/x-vhd': 'vhd',
    'application/x-xz': 'xz',
    'application/x-zip-compressed': 'zip',
    'application/x-zoo': 'zoo',
    'application/zip': 'zip',
    'application/zpaq': 'zpaq',
    "application/zstd": "zstd",
    'audio/x-ape': 'ape',
    'audio/x-shn': 'shn',
    'audio/flac': 'flac',
}

# List of programs supporting the given archive format and command.
# If command is None, the program supports all commands (list, extract, ...)
# Programs starting with "py_" are Python modules.
ArchivePrograms = {
    '7z': {
        None: ('7z', '7za', '7zr'),
        'extract': ('unar',),
    },
    'ace': {
        'extract': ('unace', 'unar'),
        'test': ('unace',),
        'list': ('unace',),
    },
    'adf': {
        'extract': ('unadf',),
        'test': ('unadf',),
        'list': ('unadf',),
    },
    'alzip': {
        'extract': ('unalz',),
        'test': ('unalz',),
        'list': ('unalz',),
    },
    'ape': {
        'create': ('mac',),
        'extract': ('mac',),
        'list': ('py_echo',),
        'test': ('mac',),
    },
    'ar': {
        None: ('ar',),
    },
    'arc': {
        None: ('arc',),
        'extract': ('nomarch',),
        'test': ('nomarch',),
        'list': ('nomarch',),
    },
    'arj': {
        None: ('arj',),
        'extract': ('7z',),
        'list': ('7z',),
        'test': ('7z',),
    },
    'bzip2': {
        None: ('7z', '7za'),
        'extract': ('pbzip2', 'lbzip2', 'bzip2', 'unar', 'py_bz2'),
        'test': ('pbzip2', 'lbzip2', 'bzip2'),
        'create': ('pbzip2', 'lbzip2', 'bzip2', 'py_bz2'),
        'list': ('py_echo',),
    },
    'bzip3': {
        'extract': ('bzip3',),
        'test': ('bzip3',),
        'create': ('bzip3',),
        'list': ('py_echo',),
    },
    'cab': {
        'extract': ('cabextract', '7z', 'unar'),
        'create': ('lcab',),
        'list': ('cabextract', '7z'),
        'test': ('cabextract', '7z'),
    },
    'chm': {
        'extract': ('7z', 'archmage', 'extract_chmLib'),
        'test': ('7z', 'archmage',),
        'list': ('7z',),
    },
    'compress': {
        'extract': ('gzip', '7z', '7za', 'unar', 'uncompress.real'),
        'list': ('7z', '7za', 'py_echo',),
        'test': ('gzip', '7z', '7za'),
        'create': ('compress',),
    },
    'cpio': {
        'extract': ('cpio', 'bsdcpio', '7z', 'unar'),
        'list': ('cpio', 'bsdcpio', '7z'),
        'test': ('cpio', 'bsdcpio', '7z',),
        'create': ('cpio', 'bsdcpio'),
    },
    'flac': {
        'extract': ('flac',),
        'test': ('flac',),
        'create': ('flac',),
        'list': ('py_echo',),
    },
    'gzip': {
        None: ('7z', '7za', 'pigz', 'gzip'),
        'extract': ('unar', 'py_gzip',),
        'create': ('zopfli', 'py_gzip'),
    },
    'iso': {
        'extract': ('7z', 'unar'),
        'list': ('7z', 'isoinfo'),
        'test': ('7z',),
        'create': ('genisoimage',),
    },
    'lz4': {
        None: ('lz4',)
    },
    'lzh': {
        None: ('lha',),
        'extract': ('lhasa', 'unar'),
    },
    'lzip': {
        'extract': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'list': ('py_echo',),
        'test': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'create': ('plzip', 'lzip', 'clzip', 'pdlzip'),
    },
    'lzma': {
        'extract': ('7z', 'lzma', 'xz', 'unar', 'py_lzma'),
        'list': ('7z', 'py_echo'),
        'test': ('7z', 'lzma', 'xz'),
        'create': ('lzma', 'xz', 'py_lzma'),
    },
    'lrzip': {
        'extract': ('lrzip',),
        'list': ('py_echo',),
        'test': ('lrzip',),
        'create': ('lrzip',),
    },
    'rar': {
        None: ('rar',),
        'extract': ('unrar', '7z', 'unar'),
        'list': ('unrar', '7z'),
        'test': ('unrar', '7z'),
    },
    'rpm': {
        'extract': ('rpm2cpio', '7z'),
        'list': ('rpm', '7z', '7za'),
        'test': ('rpm', '7z'),
    },
    'deb': {
        'extract': ('dpkg-deb', '7z'),
        'list': ('dpkg-deb', '7z'),
        'test': ('dpkg-deb', '7z'),
    },
    'dms': {
        'extract': ('xdms', 'unar'),
        'list': ('xdms',),
        'test': ('xdms',),
    },
    'lzop': {
        None: ('lzop',),
    },
    'rzip': {
        'extract': ('rzip',),
        'list': ('py_echo',),
        'create': ('rzip',),
    },
    'shar': {
        'create': ('shar',),
        'extract': ('unshar',),
    },
    'shn': {
        'extract': ('shorten',),
        'list': ('py_echo',),
        'create': ('shorten',),
    },
    'tar': {
        None: ('tar', 'star', 'bsdtar', 'py_tarfile'),
        'extract': ('unar',),
    },
    'vhd': {
        'extract': ('7z',),
        'list': ('7z',),
        'test': ('7z',),
    },
    'xz': {
        None: ('xz', '7z'),
        'extract': ('unar', 'py_lzma',),
        'create': ('py_lzma',),
    },
    'zip': {
        None: ('7z', '7za', 'py_zipfile'),
        'extract': ('unzip', 'unar', 'jar'),
        'list': ('unzip', 'jar'),
        'test': ('zip', 'unzip',),
        'create': ('zip',),
    },
    'zoo': {
        None: ('zoo',),
        'extract': ('unar',),
    },
    'zpaq': {
        None: ('zpaq',),
    },
    "zstd": {
        None: ("zstd",),
    },
}

# List of programs by archive type, which don't support password use
NoPasswordSupportArchivePrograms = {
    'bzip2': {
        None: ('7z', )
    },
    'cab': {
        None: ('7z', )
    },
    'arj': {
        None: ('7z',)
        },
    'gzip': {
        None: ('7z',)
    },
    'iso': {
        None: ('7z',)
    },
    'cpio': {
        None: ('7z', )
    },
    'rpm': {
        None: ('7z', )
    },
    'deb': {
        None: ('7z', )
    },
    'lzma': {
        None: ('7z', )
    },
    'vhd': {
        None: ('7z', )
    },
    'xz': {
        None: ('7z',)
    },
    'zip': {
        'create': ('py_zipfile',),
        'extract': ('jar',),
        'list': ('jar',),
    },
}

# List those programs that have different python module names because of
# Python module naming restrictions.
ProgramModules = {
    '7z': 'p7zip',
    '7za': 'p7azip',
    '7zr': 'p7rzip',
    'uncompress.real': 'uncompress',
    'dpkg-deb': 'dpkg',
    'extract_chmlib': 'chmlib',
}


def program_supports_compression(program, compression):
    """Decide if the given program supports the compression natively.
    @return: True iff the program supports the given compression format
      natively, else False.
    """
    if program in ('tar', ):
        if os.name == 'nt':
            return compression in ('gzip', 'bzip2')
        return compression in (
            'bzip2', 'compress', 'gzip', 'lzip', 'lzma', 'xz', 'zstd',
        )
    elif program in ('star', 'bsdtar', 'py_tarfile'):
        return compression in ('gzip', 'bzip2', 'lzma')
    return False


from .mime import guess_mime # noqa: E402

def is_archive(filename):
    """Detect if the file is a known archive."""
    mime, compression = guess_mime(filename)
    return mime in ArchiveMimetypes


def get_archive_format(filename):
    """Detect filename archive format and optional compression."""
    mime, compression = guess_mime(filename)
    if not (mime or compression):
        raise util.PatoolError(f"unknown archive format for file `{filename}'")
    if mime in ArchiveMimetypes:
        format = ArchiveMimetypes[mime]
    else:
        raise util.PatoolError(f"unknown archive mime format {mime} for file `%s' (mime-type is `{filename}')")
    if format == compression:
        # file cannot be in same format compressed
        compression = None
    return format, compression


def check_archive_format(format, compression):
    """Make sure format and compression is known."""
    if format not in ArchiveFormats:
        raise util.PatoolError(f"unknown archive format `{format}'")
    if compression is not None and compression not in ArchiveCompressions:
        raise util.PatoolError(f"unknown archive compression `{compression}'")


def find_archive_program (format, command, program=None, password=None):
    """Find suitable archive program for given format and mode."""
    commands = ArchivePrograms[format]
    programs = []
    if program is not None:
        # try a specific program first
        programs.append(program)
    # first try the universal programs with key None
    for key in (None, command):
        if key in commands:
            programs.extend(commands[key])
    if password is not None:
        programs = _remove_command_without_password_support(programs, format, command)
    if not programs:
        raise util.PatoolError(f"{command} archive format `{format}' is not supported")
    # return the first existing program
    for program in programs:
        if program.startswith('py_'):
            # it's a Python module and therefore always supported
            return program
        exe = util.find_program(program)
        if exe:
            if program == '7z' and format == 'rar' and not util.p7zip_supports_rar():
                continue
            return exe
    # no programs found
    raise util.PatoolError("could not find an executable program to %s format %s; candidates are (%s)," % (command, format, ",".join(programs)))


def _remove_command_without_password_support(programs, format, command):
    """Remove programs if they don't support work with password for current
    format and command."""
    if format not in NoPasswordSupportArchivePrograms:
        return programs
    no_password_support_commands = NoPasswordSupportArchivePrograms[format]
    no_password_support_programs = set()
    for key in (None, command):
        if key in no_password_support_commands:
            for program in no_password_support_commands[key]:
                no_password_support_programs.add(program)
    programs_with_support = []
    for program in programs:
        if program not in no_password_support_programs:
            programs_with_support.append(program)
    if not programs_with_support and programs:
        raise util.PatoolError(f"{command} archive format `{format}' with password is not supported")
    return programs_with_support


def list_formats ():
    """Print information about available archive formats to stdout."""
    print("Archive programs of", App)
    print("Archive programs are searched in the following directories:")
    print(util.system_search_path())
    print()
    for format in ArchiveFormats:
        print(format, "files:")
        for command in ArchiveCommands:
            programs = ArchivePrograms[format]
            if command not in programs and None not in programs:
                print("   %8s: - (not supported)" % command)
                continue
            try:
                program = find_archive_program(format, command)
                print("   %8s: %s" % (command, program), end=' ')
                if format == 'tar':
                    encs = [x for x in ArchiveCompressions if util.find_program(x)]
                    if encs:
                        print("(supported compressions: %s)" % ", ".join(encs), end=' ')
                elif format == '7z':
                    if util.p7zip_supports_rar():
                        print("(rar archives supported)", end=' ')
                    else:
                        print("(rar archives not supported)", end=' ')
                print()
            except util.PatoolError:
                # display information what programs can handle this archive format
                handlers = programs.get(None, programs.get(command))
                print("   %8s: - (no program found; install %s)" %
                      (command, util.strlist_with_or(handlers)))


def check_program_compression(archive, command, program, compression):
    """Check if a program supports the given compression."""
    program = os.path.basename(program)
    if compression:
        # check if compression is supported
        if not program_supports_compression(program, compression):
            if command == 'create':
                comp_command = command
            else:
                comp_command = 'extract'
            comp_prog = find_archive_program(compression, comp_command)
            if not comp_prog:
                msg = f"cannot {command} archive `{archive}': compression `{compression}' not supported"
                raise util.PatoolError(msg)


def move_outdir_orphan (outdir):
    """Move a single file or directory inside outdir a level up.
    Never overwrite files.
    Return (True, outfile) if successful, (False, reason) if not."""
    entries = os.listdir(outdir)
    if len(entries) == 1:
        src = os.path.join(outdir, entries[0])
        dst = os.path.join(os.path.dirname(outdir), entries[0])
        if os.path.exists(dst) or os.path.islink(dst):
            return (False, "local file exists")
        shutil.move(src, dst)
        os.rmdir(outdir)
        return (True, entries[0])
    return (False, "multiple files in root")


def run_archive_cmdlist (archive_cmdlist, verbosity=0):
    """Run archive command."""
    # archive_cmdlist is a command list with optional keyword arguments
    if isinstance(archive_cmdlist, tuple):
        cmdlist, runkwargs = archive_cmdlist
    else:
        cmdlist, runkwargs = archive_cmdlist, {}
    return util.run_checked(cmdlist, verbosity=verbosity, **runkwargs)


def cleanup_outdir(outdir, archive):
    """Cleanup outdir after extraction and return target file name and
    result string."""
    fileutil.make_user_readable(outdir)
    # move single directory or file in outdir
    (success, msg) = move_outdir_orphan(outdir)
    if success:
        # msg is a single directory or filename
        return msg, f"`{msg}'"
    # outdir remains unchanged
    # rename it to something more user-friendly (basically the archive
    # name without extension)
    outdir2 = fileutil.get_single_outfile("", archive)
    os.rename(outdir, outdir2)
    return outdir2, f"`{outdir2}' ({msg})"


def _extract_archive(archive, verbosity=0, interactive=True, outdir=None,
                     program=None, format=None, compression=None, password=None):
    """Extract an archive.
    @return: output directory if command is 'extract', else None
    """
    if format is None:
        format, compression = get_archive_format(archive)
    check_archive_format(format, compression)
    program = find_archive_program(format, 'extract', program=program, password=password)
    check_program_compression(archive, 'extract', program, compression)
    get_archive_cmdlist = get_archive_cmdlist_func(program, 'extract', format)
    if outdir is None:
        outdir = fileutil.tmpdir(dir=".")
        do_cleanup_outdir = True
    else:
        do_cleanup_outdir = False
        if os.path.exists(outdir):
            if not os.path.isdir(outdir):
                msg = f"output path `{outdir}' exists and is not a directory"
                raise util.PatoolError(msg)
        else:
            log.log_info(f"... creating output directory `{outdir}'.")
            os.makedirs(outdir)
    try:
        cmdlist = get_archive_cmdlist(archive, compression, program, verbosity, interactive, outdir, password=password)
        if cmdlist:
            # an empty command list means the get_archive_cmdlist() function
            # already handled the command (e.g. when it's a builtin Python
            # function)
            run_archive_cmdlist(cmdlist, verbosity=verbosity)
        if do_cleanup_outdir:
            target, msg = cleanup_outdir(outdir, archive)
        else:
            target, msg = outdir, f"`{outdir}'"
        if verbosity >= 0:
            log.log_info(f"... {archive} extracted to {msg}.")
        return target
    finally:
        # try to remove an empty temporary output directory
        if do_cleanup_outdir and os.path.isdir(outdir):
            try:
                os.rmdir(outdir)
            except OSError as err:
                if sys.exc_info()[0] is not None:
                    msg = "extraction error, could not remove temporary " \
                          f"extraction directory {outdir}: {err}"
                    log.log_error(msg)


def _create_archive(archive, filenames, verbosity=0, interactive=True,
                    program=None, format=None, compression=None, password=None):
    """Create an archive."""
    if format is None:
        format, compression = get_archive_format(archive)
    check_archive_format(format, compression)
    program = find_archive_program(format, 'create', program=program, password=password)
    check_program_compression(archive, 'create', program, compression)
    get_archive_cmdlist = get_archive_cmdlist_func(program, 'create', format)
    cmdlist = get_archive_cmdlist(archive, compression, program, verbosity, interactive, filenames, password=password)
    if cmdlist:
        # an empty command list means the get_archive_cmdlist() function
        # already handled the command (e.g. when it's a builtin Python
        # function)
        run_archive_cmdlist(cmdlist, verbosity=verbosity)


def _handle_archive(archive, command, verbosity=0, interactive=True,
                    program=None, format=None, compression=None, password=None):
    """Test and list archives."""
    if format is None:
        format, compression = get_archive_format(archive)
    check_archive_format(format, compression)
    if command not in ('list', 'test'):
        raise util.PatoolError(f"invalid archive command `{command}'")
    program = find_archive_program(format, command, program=program, password=password)
    check_program_compression(archive, command, program, compression)
    get_archive_cmdlist = get_archive_cmdlist_func(program, command, format)
    # prepare keyword arguments for command list
    cmdlist = get_archive_cmdlist(archive, compression, program, verbosity, interactive, password=password)
    if cmdlist:
        # an empty command list means the get_archive_cmdlist() function
        # already handled the command (e.g. when it's a builtin Python
        # function)
        run_archive_cmdlist(cmdlist, verbosity=verbosity)


def get_archive_cmdlist_func(program, command, format):
    """Get the Python function that executes the given program."""
    # get python module for given archive program
    key = fileutil.stripext(os.path.basename(program).lower())
    modulename = ".programs." + ProgramModules.get(key, key)
    # import the module
    try:
        module = importlib.import_module(modulename, __name__)
    except ImportError as err:
        msg = f"cannot import module {modulename} in {__name__}"
        raise util.PatoolError(msg) from err
    # get archive handler function (e.g. patoolib.programs.star.extract_tar)
    try:
        archive_cmdlist_func = getattr(module, f'{command}_{format}')
    except AttributeError as err:
        msg = f"could not find {command}_{format} in {module}"
        raise util.PatoolError(msg) from err
    def check_for_password_before_cmdlist_func_call(*args, **kwargs):
        """ If password is None, or not set, run command as usual.
        If password is set, but can't be accepted raise appropriate
        message.
        """
        if 'password' in kwargs and kwargs['password'] is None:
            kwargs.pop('password')
        if 'password' not in kwargs:
            return archive_cmdlist_func(*args, **kwargs)
        else:
            if 'password' in inspect.signature(archive_cmdlist_func).parameters:
                return archive_cmdlist_func(*args, **kwargs)
            msg = f'There is no support for password in {program}'
            raise util.PatoolError(msg)
    return check_for_password_before_cmdlist_func_call


def _diff_archives(archive1, archive2, verbosity=0, interactive=True):
    """Show differences between two archives.
    @return 0 if archives are the same, else 1
    @raises: PatoolError on errors
    """
    if fileutil.is_same_file(archive1, archive2):
        return 0
    diff = util.find_program("diff")
    if not diff:
        msg = "The diff(1) program is required for showing archive differences, please install it."
        raise util.PatoolError(msg)
    tmpdir1 = fileutil.tmpdir()
    try:
        path1 = _extract_archive(archive1, outdir=tmpdir1, verbosity=-1)
        entries1 = os.listdir(tmpdir1)
        tmpdir2 = fileutil.tmpdir()
        try:
            path2 = _extract_archive(archive2, outdir=tmpdir2, verbosity=-1)
            entries2 = os.listdir(tmpdir2)
            if len(entries1) == 1 and len(entries2) == 1:
                # when both archives only have one single entry, compare those
                diffpath1 = os.path.join(path1, entries1[0])
                diffpath2 = os.path.join(path2, entries2[0])
            else:
                diffpath1 = path1
                diffpath2 = path2
            return util.run_checked([diff, "-urN", diffpath1, diffpath2], verbosity=1, ret_ok=(0, 1))
        finally:
            fileutil.rmtree(tmpdir2)
    finally:
        fileutil.rmtree(tmpdir1)


def _search_archive(pattern, archive, verbosity=0, interactive=True, password=None):
    """Search for given pattern in an archive."""
    grep = util.find_program("grep")
    if not grep:
        msg = "The grep(1) program is required for searching archive contents, please install it."
        raise util.PatoolError(msg)
    tmpdir = fileutil.tmpdir()
    try:
        path = _extract_archive(archive, outdir=tmpdir, verbosity=-1, password=password)
        return util.run_checked([grep, "-r", "-e", pattern, "."], ret_ok=(0, 1), verbosity=1, cwd=path)
    finally:
        fileutil.rmtree(tmpdir)


def _repack_archive(archive1, archive2, verbosity=0, interactive=True, password=None):
    """Repackage an archive to a different format."""
    format1, compression1 = get_archive_format(archive1)
    format2, compression2 = get_archive_format(archive2)
    if format1 == format2 and compression1 == compression2:
        # same format and compression allows to copy the file
        fileutil.link_or_copy(archive1, archive2, verbosity=verbosity)
        return
    tmpdir = fileutil.tmpdir()
    try:
        kwargs = dict(verbosity=verbosity, outdir=tmpdir, password=password)
        same_format = (format1 == format2 and compression1 and compression2)
        if same_format:
            # only decompress since the format is the same
            kwargs['format'] = compression1
        path = _extract_archive(archive1, **kwargs)
        archive = os.path.abspath(archive2)
        files = tuple(os.listdir(path))
        olddir = os.getcwd()
        os.chdir(path)
        try:
            kwargs = dict(verbosity=verbosity, interactive=interactive, password=password)
            if same_format:
                # only compress since the format is the same
                kwargs['format'] = compression2
            _create_archive(archive, files, **kwargs)
        finally:
            os.chdir(olddir)
    finally:
        fileutil.rmtree(tmpdir)


# the patool library API

def extract_archive(archive, verbosity=0, outdir=None, program=None, interactive=True, password=None):
    """Extract given archive."""
    fileutil.check_existing_filename(archive)
    if verbosity >= 0:
        log.log_info(f"Extracting {archive} ...")
    return _extract_archive(archive, verbosity=verbosity, interactive=interactive, outdir=outdir, program=program, password=password)


def list_archive(archive, verbosity=1, program=None, interactive=True, password=None):
    """List given archive."""
    # Set default verbosity to 1 since the listing output should be visible.
    fileutil.check_existing_filename(archive)
    if verbosity >= 0:
        log.log_info(f"Listing {archive} ...")
    return _handle_archive(archive, 'list', verbosity=verbosity, interactive=interactive, program=program, password=password)


def test_archive(archive, verbosity=0, program=None, interactive=True, password=None):
    """Test given archive."""
    fileutil.check_existing_filename(archive)
    if verbosity >= 0:
        log.log_info(f"Testing {archive} ...")
    res = _handle_archive(archive, 'test', verbosity=verbosity,
        interactive=interactive, program=program, password=password)
    if verbosity >= 0:
        log.log_info("... tested ok.")
    return res


def create_archive(archive, filenames, verbosity=0, program=None, interactive=True, password=None):
    """Create given archive with given files."""
    fileutil.check_new_filename(archive)
    fileutil.check_archive_filelist(filenames)
    if verbosity >= 0:
        log.log_info(f"Creating {archive} ...")
    res = _create_archive(archive, filenames, verbosity=verbosity,
                          interactive=interactive, program=program, password=password)
    if verbosity >= 0:
        log.log_info(f"... {archive} created.")
    return res


def diff_archives(archive1, archive2, verbosity=0, interactive=True):
    """Print differences between two archives."""
    fileutil.check_existing_filename(archive1)
    fileutil.check_existing_filename(archive2)
    if verbosity >= 0:
        log.log_info(f"Comparing {archive1} with {archive2} ...")
    res = _diff_archives(archive1, archive2, verbosity=verbosity, interactive=interactive)
    if res == 0 and verbosity >= 0:
        log.log_info("... no differences found.")
    return res


def search_archive(pattern, archive, verbosity=0, interactive=True, password=None):
    """Search pattern in archive members."""
    if not pattern:
        raise util.PatoolError("empty search pattern")
    fileutil.check_existing_filename(archive)
    if verbosity >= 0:
        log.log_info(f"Searching {pattern!r} in {archive} ...")
    res = _search_archive(pattern, archive, verbosity=verbosity, interactive=interactive, password=password)
    if res == 1 and verbosity >= 0:
        log.log_info(f"... {pattern!r} not found")
    return res


def repack_archive(archive, archive_new, verbosity=0, interactive=True, password=None):
    """Repack archive to different file and/or format."""
    fileutil.check_existing_filename(archive)
    fileutil.check_new_filename(archive_new)
    if verbosity >= 0:
        log.log_info(f"Repacking {archive} to {archive_new} ...")
    res = _repack_archive(archive, archive_new, verbosity=verbosity, interactive=interactive, password=password)
    if verbosity >= 0:
        log.log_info("... repacking successful.")
    return res
