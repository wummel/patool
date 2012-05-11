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
import os
import shutil
import stat
from patoolib import util

# Supported archive commands
ArchiveCommands = ('list', 'extract', 'test', 'create')

# Supported archive formats
ArchiveFormats = ('7z', 'ace', 'alzip', 'ar', 'arc', 'arj', 'bzip2',
    'cab', 'compress', 'cpio', 'deb', 'dms', 'gzip', 'lrzip', 'lzh', 'lzip', 'lzma',
    'lzop', 'rar', 'rpm', 'rzip', 'tar', 'xz', 'zip', 'zoo')

# Supported encodings (used with tar for example)
# Note that all encodings must also be archive formats
ArchiveEncodings = ('bzip2', 'compress', 'gzip', 'lzip', 'lzma', 'xz')

# Map MIME types to archive format
ArchiveMimetypes = {
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
}

# List of programs supporting the given encoding

EncodingPrograms = {
    'gzip': ('pigz', 'gzip'),
    'bzip2': ('pbzip2', 'lbzip2', 'bzip2'),
    'compress': ('compress',),
    'lzma': ('lzma',),
    'xz': ('xz',),
    'lzip': ('lzip', 'clzip', 'plzip', 'pdlzip'),
}

# List of programs supporting the given archive format and command.
# If command is None, the program supports all commands (list, extract, ...)
ArchivePrograms = {
    'ace': {
        'extract': ('unace',),
        'test': ('unace',),
        'list': ('unace',),
    },
    'alzip': {
        'extract': ('unalz',),
        'test': ('unalz',),
        'list': ('unalz',),
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
        'extract': ('pbzip2', 'lbzip2', 'bzip2', '7z', '7za'),
        'test': ('pbzip2', 'lbzip2', 'bzip2', '7z', '7za'),
        'create': ('pbzip2', 'lbzip2', 'bzip2', '7z', '7za'),
        'list': ('7z', '7za', 'echo',),
    },
    'tar': {
        None: ('tar', 'star',),
    },
    'zip': {
        'extract': ('unzip', '7z', '7za'),
        'list': ('unzip', '7z', '7za'),
        'test': ('unzip', '7z', '7za'),
        'create': ('zip', '7z', '7za'),
    },
    'gzip': {
        None: ('pigz', 'gzip', '7z', '7za'),
    },
    'lzh': {
        None: ('lha',),
    },
    'lzip': {
        'extract': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'list': ('echo',),
        'test': ('plzip', 'lzip', 'clzip', 'pdlzip'),
        'create': ('plzip', 'lzip', 'clzip', 'pdlzip'),
    },
    'lrzip': {
        'extract': ('lrzip',),
        'list': ('echo',),
        'test': ('lrzip',),
        'create': ('lrzip',),
    },
    'compress': {
        'extract': ('gzip', '7z', '7za', 'uncompress.real'),
        'list': ('7z', '7za', 'echo',),
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
    'cab': {
        'extract': ('cabextract', '7z', 'orange'),
        'list': ('cabextract', '7z'),
        'test': ('cabextract', '7z'),
    },
    'arj': {
        None: ('arj',),
        'extract': ('7z',),
        'list': ('7z',),
        'test': ('7z',),
    },
    'cpio': {
        'extract': ('cpio', '7z'),
        'list': ('cpio', '7z'),
        'test': ('7z',),
        'create': ('cpio',),
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
        'extract': ('lzma',),
        'list': ('echo',),
        'test': ('lzma',),
        'create': ('lzma',),
    },
    'rzip': {
        'extract': ('rzip',),
        'list': ('echo',),
        'create': ('rzip',),
    },
    'xz': {
        None: ('xz',),
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
}


def get_archive_format (filename):
    """Detect filename archive format and optional encoding."""
    mime, encoding = util.guess_mime(filename)
    if not (mime or encoding):
        raise util.PatoolError("unknown archive format for file `%s'" % filename)
    if mime in ArchiveMimetypes:
        format = ArchiveMimetypes[mime]
    else:
        raise util.PatoolError("unknown archive format for file `%s' (mime-type is `%s')" % (filename, mime))
    if format == encoding:
        # file cannot be in same format encoded
        encoding = None
    return format, encoding


def check_archive_format (format, encoding):
    """Make sure format and encoding is known."""
    if format not in ArchiveFormats:
        raise util.PatoolError("unknown archive format `%s'" % format)
    if encoding is not None and encoding not in ArchiveEncodings:
        raise util.PatoolError("unkonwn archive encoding `%s'" % encoding)


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
        exe = util.find_program(program)
        if exe:
            if program == '7z' and format == 'rar' and not util.p7zip_supports_rar():
                continue
            return exe
    # no programs found
    raise util.PatoolError("could not find an executable program to %s format %s; candidates are (%s)," % (command, format, ",".join(programs)))


def find_encoding_program (program, encoding):
    """Find suitable encoding program and return it. Returns None if
    no encoding program could be found"""
    if program in ('tar', 'star'):
        for enc_program in EncodingPrograms[encoding]:
            found = util.find_program(enc_program)
            if found:
                return found
    return None


def list_formats ():
    """Print information about available archive formats to stdout."""
    for format in ArchiveFormats:
        print format, "files:"
        for command in ArchiveCommands:
            programs = ArchivePrograms[format]
            if command not in programs and None not in programs:
                print "   %8s: - (not supported)" % command
                continue
            try:
                program = find_archive_program(format, command)
                print "   %8s: %s" % (command, program),
                if format == 'tar':
                    encs = [x for x in ArchiveEncodings if util.find_program(x)]
                    if encs:
                        print "(supported encodings: %s)" % ", ".join(encs),
                elif format == '7z':
                    if util.p7zip_supports_rar():
                        print "(rar archives supported)",
                    else:
                        print "(rar archives not supported)",
                print
            except util.PatoolError:
                handlers = programs.get(None, programs.get(command))
                print "   %8s: - (no program found; install %s)" % \
                      (command, util.strlist_with_or(handlers))
    return 0


AllowedConfigKeys = ("verbose", "program")

def clean_config_keys (kwargs):
    """Remove invalid configuration keys from arguments."""
    config_kwargs = dict(kwargs)
    for key in kwargs:
        if key not in AllowedConfigKeys:
            del config_kwargs[key]
    return config_kwargs


def parse_config (archive, format, encoding, command, **kwargs):
    """The configuration determines which program to use for which
    archive format for the given command.
    @raises: PatoolError if command for given format and encoding
       is not supported.
    """
    config = {
        'verbose': False,
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
    if encoding and not find_encoding_program(program, encoding):
        msg = "cannot %s archive `%s': encoding `%s' not supported by %s" % \
              (command, archive, encoding, program)
        raise util.PatoolError(msg)
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


def run_archive_cmdlist (archive_cmdlist):
    """Run archive command."""
    # archive_cmdlist is a command list with optional keyword arguments
    if isinstance(archive_cmdlist, tuple):
        cmdlist, runkwargs = archive_cmdlist
    else:
        cmdlist, runkwargs = archive_cmdlist, {}
    util.run_checked(cmdlist, **runkwargs)


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


def cleanup_outdir (outdir):
    """Cleanup outdir after extraction and return target file name and
    result string."""
    make_user_readable(outdir)
    # move single directory or file in outdir
    (success, msg) = move_outdir_orphan(outdir)
    if success:
        # msg is a single directory or filename
        return msg, "`%s'" % msg
    # outdir remains unchanged
    return outdir, "`%s' (%s)" % (outdir, msg)


def _handle_archive (archive, command, *args, **kwargs):
    """Handle archive command; raising PatoolError on errors."""
    if command != 'create':
        # check that archive is a regular file
        util.check_filename(archive)
    format, encoding = kwargs.get("format"), kwargs.get("encoding")
    if format is None:
        format, encoding = get_archive_format(archive)
    check_archive_format(format, encoding)
    check_archive_command(command)
    config_kwargs = clean_config_keys(kwargs)
    config = parse_config(archive, format, encoding, command, **config_kwargs)
    # check if archive already exists
    if command == 'create' and os.path.exists(archive):
        raise util.PatoolError("archive `%s' already exists" % archive)
    program = config['program']
    get_archive_cmdlist = get_archive_cmdlist_func(program, command, format)
    # prepare keyword arguments for command list
    cmd_kwargs = dict(verbose=config['verbose'])
    origarchive = None
    if command == 'extract':
        if "outdir" in kwargs:
            cmd_kwargs["outdir"] = kwargs["outdir"]
            do_cleanup_outdir = False
        else:
            cmd_kwargs['outdir'] = util.tmpdir(dir=os.getcwd())
            do_cleanup_outdir = True
    elif command == 'create' and os.path.basename(program) == 'arc' and \
         ".arc" in archive and not archive.endswith(".arc"):
        # the arc program mangles the archive name if it contains ".arc"
        origarchive = archive
        archive = util.tmpfile(dir=os.path.dirname(archive), suffix=".arc")
    try:
        cmdlist = get_archive_cmdlist(archive, encoding, program, *args, **cmd_kwargs)
        run_archive_cmdlist(cmdlist)
        if command == 'extract':
            if do_cleanup_outdir:
                target, msg = cleanup_outdir(cmd_kwargs["outdir"])
                util.log_info("%s extracted to %s" % (archive, msg))
            else:
                target, msg = cmd_kwargs["outdir"], "`%s'" % cmd_kwargs["outdir"]
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
    # get python module for given archive program
    key = util.stripext(os.path.basename(program).lower())
    module = ProgramModules.get(key, key)
    # import archive handler function (eg. patoolib.programs.star.extract_tar)
    args = (module, command, format)
    import_cmd = "from patoolib.programs.%s import %s_%s as func" % args
    try:
        exec import_cmd
    except ImportError:
        raise util.PatoolError('ImportError executing %r' % import_cmd)
    return locals()['func']


def rmtree_log_error (func, path, exc):
    """Error function for shutil.rmtree(). Raises a PatoolError."""
    msg = "Error in %s(%s): %s" % (func.__name__, path, str(exc[1]))
    util.log_error(msg)


def _diff_archives (archive1, archive2, **kwargs):
    """Show differences between two archives."""
    diff = util.find_program("diff")
    if not diff:
        raise util.PatoolError("The diff(1) program is required for showing archive differences, please install it")
    tmpdir1 = util.tmpdir()
    tmpdir2 = util.tmpdir()
    try:
        path1 = _handle_archive(archive1, 'extract', outdir=tmpdir1, **kwargs)
        path2 = _handle_archive(archive2, 'extract', outdir=tmpdir2, **kwargs)
        return util.run([diff, "-urN", path1, path2])
    finally:
        shutil.rmtree(tmpdir1, onerror=rmtree_log_error)
        shutil.rmtree(tmpdir2, onerror=rmtree_log_error)


def _repack_archive (archive1, archive2, **kwargs):
    """Repackage an archive to a different format."""
    tmpdir = util.tmpdir()
    try:
        _handle_archive(archive1, 'extract', outdir=tmpdir, **kwargs)
        archive = os.path.abspath(archive2)
        files = tuple(os.listdir(tmpdir))
        os.chdir(tmpdir)
        _handle_archive(archive, 'create', *files, **kwargs)
        return 0
    finally:
        shutil.rmtree(tmpdir, onerror=rmtree_log_error)


def handle_archive (archive, command, *args, **kwargs):
    """Handle archive file command; with nice error reporting."""
    try:
        if command == "diff":
            res = _diff_archives(archive, args[0])
        elif command == "repack":
            res = _repack_archive(archive, args[0])
        else:
            _handle_archive(archive, command, *args, **kwargs)
            res = 0
    except KeyboardInterrupt:
        util.log_error("aborted")
        res = 1
    except util.PatoolError, msg:
        util.log_error(msg)
        res = 1
    except StandardError, msg:
        util.log_internal_error()
        res = 1
    return res


# convenience functions

def extract (archive, verbose=False, outdir=None):
    """Extract given archive."""
    return handle_archive(archive, 'extract', verbose=verbose, outdir=outdir)


def list (archive, verbose=False):
    """List given archive."""
    return handle_archive(archive, 'list', verbose=verbose)


def test (archive, verbose=False):
    """Test given archive."""
    return handle_archive(archive, 'test', verbose=verbose)


def create (archive, *files, **kwargs):
    """Create given archive with given files."""
    return handle_archive(archive, 'create', *files, **kwargs)


def diff (archive1, archive2, verbose=False):
    """Print differences between two archives."""
    return handle_archive(archive1, 'diff', archive2, verbose=verbose)


def repack (archive1, archive2, verbose=False):
    """Repacke archive to different file and/or format."""
    return handle_archive(archive1, 'repack', archive2, verbose=verbose)
