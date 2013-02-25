# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Bastian Kleineidam
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
from __future__ import print_function
import sys
if not hasattr(sys, "version_info") or sys.version_info < (2, 7, 0, "final", 0):
    raise SystemExit("This program requires Python 2.7 or later.")
import os
import shutil
import stat
import importlib
from . import util
__all__ = ['list_formats', 'list_archive', 'extract_archive', 'test_archive',
    'create_archive', 'diff_archives', 'search_archive', 'repack_archive']


# Supported archive commands
ArchiveCommands = ('list', 'extract', 'test', 'create')

# Supported archive formats
ArchiveFormats = (
    '7z', 'ace', 'adf', 'alzip', 'ape', 'ar', 'arc', 'arj',
    'bzip2', 'cab', 'chm', 'compress', 'cpio', 'deb', 'dms',
    'flac', 'gzip', 'lrzip', 'lzh', 'lzip', 'lzma', 'lzop',
    'rar', 'rpm', 'rzip', 'shar', 'shn', 'tar', 'xz',
    'zip', 'zoo')

# Supported compressions (used with tar for example)
# Note that all compressions must also be archive formats
ArchiveCompressions = ('bzip2', 'compress', 'gzip', 'lzip', 'lzma', 'xz')

# Map MIME types to archive format
ArchiveMimetypes = {
    'application/x-adf': 'adf',
    'application/x-bzip2': 'bzip2',
    'application/x-tar': 'tar',
    'application/x-gzip': 'gzip',
    'application/zip': 'zip',
    'application/x-zip-compressed': 'zip',
    'application/java-archive': 'zip',
    'application/x-7z-compressed': '7z',
    'application/x-compress': 'compress',
    'application/x-rar': 'rar',
    'application/rar': 'rar',
    'application/x-cab': 'cab',
    'application/vnd.ms-cab-compressed': 'cab',
    'application/x-arj': 'arj',
    'application/x-chm': 'chm',
    'application/x-cpio': 'cpio',
    'application/x-redhat-package-manager': 'rpm',
    'application/x-rpm': 'rpm',
    'application/x-debian-package': 'deb',
    'application/x-lzop': 'lzop',
    'application/x-lzma': 'lzma',
    'application/x-xz': 'xz',
    'application/x-lzip': 'lzip',
    'application/x-ace': 'ace',
    'application/x-archive': 'ar',
    'application/x-lha': 'lzh',
    'application/x-lzh': 'lzh',
    'application/x-alzip': 'alzip',
    'application/x-arc': 'arc',
    'application/x-lrzip': 'lrzip',
    'application/x-rzip': 'rzip',
    'application/x-zoo': 'zoo',
    'application/x-dms': 'dms',
    'application/x-shar': 'shar',
    'audio/x-ape': 'ape',
    'audio/x-shn': 'shn',
    'audio/flac': 'flac',
}

try:
    # use Python 3 lzma module if available
    import lzma
    py_lzma = ('py_lzma',)
except ImportError:
    py_lzma = ()

# List of programs supporting the given archive format and command.
# If command is None, the program supports all commands (list, extract, ...)
# Programs starting with "py_" are Python modules.
ArchivePrograms = {
    'ace': {
        'extract': ('unace',),
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
    'bzip2': {
        'extract': ('pbzip2', 'lbzip2', 'bzip2', '7z', '7za', 'py_bz2'),
        'test': ('pbzip2', 'lbzip2', 'bzip2', '7z', '7za'),
        'create': ('pbzip2', 'lbzip2', 'bzip2', 'py_bz2'),
        'list': ('py_echo', '7z', '7za'),
    },
    'cab': {
        'extract': ('cabextract', '7z'),
        'create': ('lcab',),
        'list': ('cabextract', '7z'),
        'test': ('cabextract', '7z'),
    },
    'chm': {
        'extract': ('archmage', 'extract_chmLib'),
        'test': ('archmage',),
    },
    'flac': {
        'extract': ('flac',),
        'test': ('flac',),
        'create': ('flac',),
        'list': ('py_echo',),
    },
    'tar': {
        None: ('tar', 'star', 'bsdtar', 'py_tarfile'),
    },
    'zip': {
        None: ('7z', '7za', 'py_zipfile'),
        'extract': ('unzip',),
        'list': ('unzip',),
        'test': ('zip', 'unzip',),
        'create': ('zip',),
    },
    'gzip': {
        None: ('7z', '7za', 'pigz', 'gzip'),
        'extract': ('py_gzip',),
        'create': ('py_gzip',),
    },
    'lzh': {
        None: ('lha',),
        'extract': ('lhasa',),
    },
    'lzip': {
        'extract': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'list': ('py_echo',),
        'test': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'create': ('plzip', 'lzip', 'clzip', 'pdlzip'),
    },
    'lrzip': {
        'extract': ('lrzip',),
        'list': ('py_echo',),
        'test': ('lrzip',),
        'create': ('lrzip',),
    },
    'compress': {
        'extract': ('gzip', '7z', '7za', 'uncompress.real'),
        'list': ('7z', '7za', 'py_echo',),
        'test': ('gzip', '7z', '7za'),
        'create': ('compress',),
    },
    '7z': {
        None: ('7z', '7za'),
    },
    'rar': {
        None: ('rar',),
        'extract': ('unrar', '7z'),
        'list': ('unrar', '7z'),
        'test': ('unrar', '7z'),
    },
    'arj': {
        None: ('arj',),
        'extract': ('7z',),
        'list': ('7z',),
        'test': ('7z',),
    },
    'cpio': {
        'extract': ('cpio', 'bsdcpio', '7z'),
        'list': ('cpio', 'bsdcpio', '7z'),
        'test': ('cpio', 'bsdcpio', '7z',),
        'create': ('cpio', 'bsdcpio'),
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
    'lzop': {
        None: ('lzop',),
    },
    'lzma': {
        'extract': ('lzma',) + py_lzma,
        'list': ('py_echo',),
        'test': ('lzma',),
        'create': ('lzma',) + py_lzma,
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
    'xz': {
        None: ('xz',),
        'extract': py_lzma,
        'create': py_lzma,
    },
    'zoo': {
        None: ('zoo',),
    },
    'dms': {
        'extract': ('xdms',),
        'list': ('xdms',),
        'test': ('xdms',),
    },
}

# List those programs that have different python module names because of
# Python module naming restrictions.
ProgramModules = {
    '7z': 'p7zip',
    '7za': 'p7azip',
    'uncompress.real': 'uncompress',
    'dpkg-deb': 'dpkg',
    'extract_chmlib': 'chmlib',
}


def get_archive_format (filename):
    """Detect filename archive format and optional compression."""
    mime, compression = util.guess_mime(filename)
    if not (mime or compression):
        raise util.PatoolError("unknown archive format for file `%s'" % filename)
    if mime in ArchiveMimetypes:
        format = ArchiveMimetypes[mime]
    else:
        raise util.PatoolError("unknown archive format for file `%s' (mime-type is `%s')" % (filename, mime))
    if format == compression:
        # file cannot be in same format compressed
        compression = None
    return format, compression


def check_archive_format (format, compression):
    """Make sure format and compression is known."""
    if format not in ArchiveFormats:
        raise util.PatoolError("unknown archive format `%s'" % format)
    if compression is not None and compression not in ArchiveCompressions:
        raise util.PatoolError("unkonwn archive compression `%s'" % compression)


def check_archive_command (command):
    """Make sure archive command is valid."""
    if command not in ArchiveCommands:
        raise util.PatoolError("invalid archive command `%s'" % command)


def find_archive_program (format, command):
    """Find suitable archive program for given format and mode."""
    commands = ArchivePrograms[format]
    programs = []
    # first try the universal programs with key None
    for key in (None, command):
        if key in commands:
            programs.extend(commands[key])
    if not programs:
        raise util.PatoolError("%s archive format `%s' is not supported" % (command, format))
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


def program_supports_compression (program, compression):
    """Decide if the given program supports the compression natively.
    @return: True iff the program supports the given compression format
      natively, else False.
    """
    if program in ('tar', 'star', 'bsdtar', 'py_tarfile'):
        return compression in ('gzip', 'bzip2')
    return False


def list_formats ():
    """Print information about available archive formats to stdout."""
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
                handlers = programs.get(None, programs.get(command))
                print("   %8s: - (no program found; install %s)" %
                      (command, util.strlist_with_or(handlers)))


AllowedConfigKeys = ("verbosity", "program")

def clean_config_keys (kwargs):
    """Remove invalid configuration keys from arguments."""
    config_kwargs = dict(kwargs)
    for key in kwargs:
        if key not in AllowedConfigKeys:
            del config_kwargs[key]
    return config_kwargs


def parse_config (archive, format, compression, command, **kwargs):
    """The configuration determines which program to use for which
    archive format for the given command.
    @raises: PatoolError if command for given format and compression
       is not supported.
    """
    config = {
        'verbosity': 0,
    }
    config['program'] = find_archive_program(format, command)
    for key, value in kwargs.items():
        if value is not None:
            if key == 'program':
                program = util.find_program(value)
                if program:
                    value = program
            config[key] = value
    program = os.path.basename(config['program'])
    if compression:
        # check if compression is supported
        if not program_supports_compression(program, compression):
            if command == 'create':
                comp_command = command
            else:
                comp_command = 'extract'
            comp_prog = find_archive_program(compression, comp_command)
            if not comp_prog:
                msg = "cannot %s archive `%s': compression `%s' not supported"
                raise util.PatoolError(msg % (command, archive, compression))
    return config


def move_outdir_orphan (outdir):
    """Move a single file or directory inside outdir a level up.
    Never overwrite files.
    Return (True, outfile) if successful, (False, reason) if not."""
    entries = os.listdir(outdir)
    if len(entries) == 1:
        src = os.path.join(outdir, entries[0])
        dst = os.path.join(os.path.dirname(outdir), entries[0])
        if os.path.exists(dst):
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


def make_file_readable (filename):
    """Make file user readable if it is not a link."""
    if not os.path.islink(filename):
        util.set_mode(filename, stat.S_IRUSR)


def make_dir_readable (filename):
    """Make directory user readable and executable."""
    util.set_mode(filename, stat.S_IRUSR|stat.S_IXUSR)


def make_user_readable (directory):
    """Make all files in given directory user readable. Also recurse into
    subdirectories."""
    for root, dirs, files in os.walk(directory, onerror=util.log_error):
        for filename in files:
            make_file_readable(os.path.join(root, filename))
        for dirname in dirs:
            make_dir_readable(os.path.join(root, dirname))


def cleanup_outdir (outdir, archive):
    """Cleanup outdir after extraction and return target file name and
    result string."""
    make_user_readable(outdir)
    # move single directory or file in outdir
    (success, msg) = move_outdir_orphan(outdir)
    if success:
        # msg is a single directory or filename
        return msg, "`%s'" % msg
    # outdir remains unchanged
    # rename it to something more user-friendly (basically the archive
    # name without extension)
    outdir2 = util.get_single_outfile("", archive)
    os.rename(outdir, outdir2)
    return outdir2, "`%s' (%s)" % (outdir2, msg)


def _handle_archive (archive, command, *args, **kwargs):
    """Handle archive command; raising PatoolError on errors.
    @return: output directory if command is 'extract', else None
    """
    format, compression = kwargs.get("format"), kwargs.get("compression")
    if format is None:
        format, compression = get_archive_format(archive)
    check_archive_format(format, compression)
    check_archive_command(command)
    config_kwargs = clean_config_keys(kwargs)
    config = parse_config(archive, format, compression, command, **config_kwargs)
    program = config['program']
    get_archive_cmdlist = get_archive_cmdlist_func(program, command, format)
    # prepare keyword arguments for command list
    cmd_kwargs = dict(verbosity=config['verbosity'])
    origarchive = None
    if command == 'extract':
        if kwargs.get('outdir'):
            cmd_kwargs["outdir"] = kwargs["outdir"]
            do_cleanup_outdir = False
        else:
            cmd_kwargs['outdir'] = util.tmpdir(dir=".")
            do_cleanup_outdir = True
    elif command == 'create' and os.path.basename(program) == 'arc' and \
         ".arc" in archive and not archive.endswith(".arc"):
        # the arc program mangles the archive name if it contains ".arc"
        origarchive = archive
        archive = util.tmpfile(dir=os.path.dirname(archive), suffix=".arc")
    try:
        cmdlist = get_archive_cmdlist(archive, compression, program, *args, **cmd_kwargs)
        if cmdlist:
            # an empty command list means the get_archive_cmdlist() function
            # already handled the command (eg. when it's a builtin Python
            # function)
            run_archive_cmdlist(cmdlist, verbosity=config['verbosity'])
        if command == 'extract':
            if do_cleanup_outdir:
                target, msg = cleanup_outdir(cmd_kwargs["outdir"], archive)
            else:
                target, msg = cmd_kwargs["outdir"], "`%s'" % cmd_kwargs["outdir"]
            if config['verbosity'] >= 0:
                util.log_info("... %s extracted to %s." % (archive, msg))
            return target
        elif command == 'create' and origarchive:
            shutil.move(archive, origarchive)
    finally:
        if command == "extract":
            try:
                os.rmdir(cmd_kwargs["outdir"])
            except OSError:
                pass


def get_archive_cmdlist_func (program, command, format):
    """Get the Python function that executes the given program."""
    # get python module for given archive program
    key = util.stripext(os.path.basename(program).lower())
    modulename = ".programs." + ProgramModules.get(key, key)
    # import the module
    try:
        module = importlib.import_module(modulename, __name__)
    except ImportError as msg:
        raise util.PatoolError(msg)
    # get archive handler function (eg. patoolib.programs.star.extract_tar)
    try:
        return getattr(module, '%s_%s' % (command, format))
    except AttributeError as msg:
        raise util.PatoolError(msg)


def rmtree_log_error (func, path, exc):
    """Error function for shutil.rmtree(). Raises a PatoolError."""
    msg = "Error in %s(%s): %s" % (func.__name__, path, str(exc[1]))
    util.log_error(msg)


def _diff_archives (archive1, archive2, verbosity=0):
    """Show differences between two archives.
    @return 0 if archives are the same, else 1
    @raises: PatoolError on errors
    """
    if util.is_same_file(archive1, archive2):
        return 0
    diff = util.find_program("diff")
    if not diff:
        msg = "The diff(1) program is required for showing archive differences, please install it."
        raise util.PatoolError(msg)
    tmpdir1 = util.tmpdir()
    try:
        path1 = _handle_archive(archive1, 'extract', outdir=tmpdir1, verbosity=-1)
        tmpdir2 = util.tmpdir()
        try:
            path2 = _handle_archive(archive2, 'extract', outdir=tmpdir2, verbosity=-1)
            return util.run_checked([diff, "-urN", path1, path2], verbosity=1, ret_ok=(0, 1))
        finally:
            shutil.rmtree(tmpdir2, onerror=rmtree_log_error)
    finally:
        shutil.rmtree(tmpdir1, onerror=rmtree_log_error)


def _search_archive(pattern, archive, verbosity=0):
    """Search for given pattern in an archive."""
    grep = util.find_program("grep")
    if not grep:
        msg = "The grep(1) program is required for searching archive contents, please install it."
        raise util.PatoolError(msg)
    tmpdir = util.tmpdir()
    try:
        path = _handle_archive(archive, 'extract', outdir=tmpdir, verbosity=-1)
        return util.run_checked([grep, "-r", "-e", pattern, "."], ret_ok=(0, 1), verbosity=1, cwd=path)
    finally:
        shutil.rmtree(tmpdir, onerror=rmtree_log_error)


def _repack_archive (archive1, archive2, verbosity=0):
    """Repackage an archive to a different format."""
    format1, compression1 = get_archive_format(archive1)
    format2, compression2 = get_archive_format(archive2)
    if format1 == format2 and compression1 == compression2:
        # same format and compression allows to copy the file
        util.link_or_copy(archive1, archive2, verbosity=verbosity)
        return
    tmpdir = util.tmpdir()
    try:
        kwargs = dict(verbosity=verbosity, outdir=tmpdir)
        same_format = (format1 == format2 and compression1 and compression2)
        if same_format:
            # only decompress since the format is the same
            kwargs['format'] = compression1
        path = _handle_archive(archive1, 'extract', **kwargs)
        archive = os.path.abspath(archive2)
        files = tuple(os.listdir(path))
        olddir = os.getcwd()
        os.chdir(path)
        try:
            if same_format:
                # only compress since the format is the same
                kwargs['format'] = compression2
            _handle_archive(archive, 'create', *files, **kwargs)
        finally:
            os.chdir(olddir)
    finally:
        shutil.rmtree(tmpdir, onerror=rmtree_log_error)


# the patool library API

def extract_archive(archive, verbosity=0, outdir=None, program=None):
    """Extract given archive."""
    util.check_existing_filename(archive)
    if verbosity >= 0:
        util.log_info("Extracting %s ..." % archive)
    return _handle_archive(archive, 'extract', verbosity=verbosity, outdir=outdir, program=program)


def list_archive(archive, verbosity=0, program=None):
    """List given archive."""
    util.check_existing_filename(archive)
    if verbosity >= 0:
        util.log_info("Listing %s ..." % archive)
    return _handle_archive(archive, 'list', verbosity=verbosity, program=program)


def test_archive(archive, verbosity=0, program=None):
    """Test given archive."""
    util.check_existing_filename(archive)
    if verbosity >= 0:
        util.log_info("Testing %s ..." % archive)
    res = _handle_archive(archive, 'test', verbosity=verbosity, program=program)
    if verbosity >= 0:
        util.log_info("... tested ok.")
    return res


def create_archive(archive, filenames, verbosity=0, program=None):
    """Create given archive with given files."""
    util.check_new_filename(archive)
    util.check_archive_filelist(filenames)
    if verbosity >= 0:
        util.log_info("Creating %s ..." % archive)
    res = _handle_archive(archive, 'create', *tuple(filenames), verbosity=verbosity, program=program)
    if verbosity >= 0:
        util.log_info("... %s created." % archive)
    return res


def diff_archives(archive1, archive2, verbosity=0):
    """Print differences between two archives."""
    util.check_existing_filename(archive1)
    util.check_existing_filename(archive2)
    if verbosity >= 0:
        util.log_info("Comparing %s with %s ..." % (archive1, archive2))
    res = _diff_archives(archive1, archive2, verbosity=verbosity)
    if res == 0 and verbosity >= 0:
        util.log_info("... no differences found.")


def search_archive(pattern, archive, verbosity=0):
    """Search pattern in archive members."""
    if not pattern:
        raise util.PatoolError("empty search pattern")
    util.check_existing_filename(archive)
    if verbosity >= 0:
        util.log_info("Searching %r in %s ..." % (pattern, archive))
    res = _search_archive(pattern, archive, verbosity=verbosity)
    if res == 1 and verbosity >= 0:
        util.log_info("... %r not found" % pattern)
    return res


def repack_archive (archive, archive_new, verbosity=0):
    """Repack archive to different file and/or format."""
    util.check_existing_filename(archive)
    util.check_new_filename(archive_new)
    if verbosity >= 0:
        util.log_info("Repacking %s to %s ..." % (archive, archive_new))
    res = _repack_archive(archive, archive_new, verbosity=verbosity)
    if verbosity >= 0:
        util.log_info("... repacking successful.")
    return res
