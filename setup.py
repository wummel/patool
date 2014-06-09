#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2014 Bastian Kleineidam
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
"""
Setup file for the distuils module.
"""
from __future__ import print_function
import sys
if not hasattr(sys, "version_info") or sys.version_info < (2, 7, 0, "final", 0):
    raise SystemExit("This program requires Python 2.7 or later.")
import os
import re
import shutil
import glob
import subprocess
try:
    from cx_Freeze import setup, Executable
except ImportError:
    from distutils.core import setup
try:
    # py2exe monkey-patches the distutils.core.Distribution class
    # So we need to import it before importing the Distribution class
    import py2exe
    has_py2exe = True
except ImportError:
    # py2exe is not installed
    has_py2exe = False
try:
    from cx_Freeze.dist import Distribution
    executables = [Executable("patool")]
except ImportError:
    from distutils.core import Distribution
    executables = None
from distutils.command.install_lib import install_lib
from distutils import util
from distutils.file_util import write_file

AppName = "patool"
AppVersion = "1.6"
MyName = "Bastian Kleineidam"
MyEmail = "bastian.kleineidam@web.de"

py_excludes = ['doctest', 'unittest', 'Tkinter', '_ssl', 'pdb',
  'email', 'calendar', 'ftplib', 'httplib', 'pickle', 'optparse','rfc822'
]
# py2exe options for Windows packaging
py2exe_options = dict(
    packages=["encodings", 'patoolib.programs'],
    excludes=py_excludes,
    # silence py2exe error about not finding msvcp90.dll
    dll_excludes=['MSVCP90.dll'],
    compressed=1,
    optimize=2,
)
# cx_Freeze for Linux RPM packaging
cxfreeze_options = dict(
    packages=["encodings", 'patoolib.programs'],
    excludes=py_excludes,
)

# Microsoft Visual C++ runtime version (tested with Python 2.7.2)
MSVCP90Version = '9.0.21022.8'
MSVCP90Token = '1fc8b3b9a1e18e3b'


def normpath (path):
    """Norm a path name to platform specific notation."""
    return os.path.normpath(path)


def cnormpath (path):
    """Norm a path name to platform specific notation and make it absolute."""
    path = normpath(path)
    if os.name == 'nt':
        # replace slashes with backslashes
        path = path.replace("/", "\\")
    if not os.path.isabs(path):
        path = normpath(os.path.join(sys.prefix, path))
    return path


release_ro = re.compile(r"\(released (.+)\)")
def get_release_date ():
    """Parse and return relase date as string from doc/changelog.txt."""
    fname = os.path.join("doc", "changelog.txt")
    release_date = "unknown"
    with open(fname) as fd:
        # the release date is on the first line
        line = fd.readline()
        mo = release_ro.search(line)
        if mo:
            release_date = mo.groups(1)
    return release_date


data_files = []
if os.name == 'nt':
    data_files.append(('share', ['doc/patool.txt']))
else:
    data_files.append(('share/man/man1', ['doc/patool.1']))


def get_nt_platform_vars ():
    """Return program file path and architecture for NT systems."""
    platform = util.get_platform()
    if platform == "win-amd64":
        # the Visual C++ runtime files are installed in the x86 directory
        progvar = "%ProgramFiles(x86)%"
        architecture = "amd64"
    elif platform == "win32":
        progvar = "%ProgramFiles%"
        architecture = "x86"
    else:
        raise ValueError("Unsupported platform %r" % platform)
    return os.path.expandvars(progvar), architecture


def add_msvc_files (files):
    """Add needed MSVC++ runtime files. Only Version 9.0.21022.8 is tested
    and can be downloaded here:
    http://www.microsoft.com/en-us/download/details.aspx?id=29
    """
    prog_dir, architecture = get_nt_platform_vars()
    dirname = "Microsoft.VC90.CRT"
    version = "%s_%s_x-ww_d08d0375" % (MSVCP90Token, MSVCP90Version)
    args = (architecture, dirname, version)
    path = r'C:\Windows\WinSxS\%s_%s_%s\*.*' % args
    files.append((dirname, glob.glob(path)))
    # Copy the manifest file into the build directory and rename it
    # because it must have the same name as the directory.
    path = r'C:\Windows\WinSxS\Manifests\%s_%s_%s.manifest' % args
    target = os.path.join(os.getcwd(), 'build', '%s.manifest' % dirname)
    shutil.copy(path, target)
    files.append((dirname, [target]))


if 'py2exe' in sys.argv[1:]:
    if not has_py2exe:
        raise SystemExit("py2exe module could not be imported")
    add_msvc_files(data_files)


class MyInstallLib (install_lib, object):
    """Custom library installation."""

    def install (self):
        """Install the generated config file."""
        outs = super(MyInstallLib, self).install()
        infile = self.create_conf_file()
        outfile = os.path.join(self.install_dir, os.path.basename(infile))
        self.copy_file(infile, outfile)
        outs.append(outfile)
        return outs

    def create_conf_file (self):
        """Create configuration file."""
        cmd_obj = self.distribution.get_command_obj("install")
        cmd_obj.ensure_finalized()
        # we have to write a configuration file because we need the
        # <install_data> directory (and other stuff like author, url, ...)
        # all paths are made absolute by cnormpath()
        data = []
        for d in ['purelib', 'platlib', 'lib', 'headers', 'scripts', 'data']:
            attr = 'install_%s' % d
            if cmd_obj.root:
                # cut off root path prefix
                cutoff = len(cmd_obj.root)
                # don't strip the path separator
                if cmd_obj.root.endswith(os.sep):
                    cutoff -= 1
                val = getattr(cmd_obj, attr)[cutoff:]
            else:
                val = getattr(cmd_obj, attr)
            if attr == 'install_data':
                cdir = os.path.join(val, "share", "dosage")
                data.append('config_dir = %r' % cnormpath(cdir))
            elif attr == 'install_lib':
                if cmd_obj.root:
                    _drive, tail = os.path.splitdrive(val)
                    if tail.startswith(os.sep):
                        tail = tail[1:]
                    self.install_lib = os.path.join(cmd_obj.root, tail)
                else:
                    self.install_lib = val
            data.append("%s = %r" % (attr, cnormpath(val)))
        self.distribution.create_conf_file(data, directory=self.install_lib)
        return self.get_conf_output()

    def get_conf_output (self):
        """Get filename for distribution configuration file."""
        return self.distribution.get_conf_filename(self.install_lib)

    def get_outputs (self):
        """Add the generated config file to the list of outputs."""
        outs = super(MyInstallLib, self).get_outputs()
        conf_output = self.get_conf_output()
        outs.append(conf_output)
        if self.compile:
            outs.extend(self._bytecode_filenames([conf_output]))
        return outs


class MyDistribution (Distribution, object):
    """Custom distribution class generating config file."""

    def __init__ (self, attrs):
        """Set console and windows scripts."""
        super(MyDistribution, self).__init__(attrs)
        self.console = ['patool']

    def run_commands (self):
        """Generate config file and run commands."""
        cwd = os.getcwd()
        data = []
        data.append('config_dir = %r' % os.path.join(cwd, "config"))
        data.append("install_data = %r" % cwd)
        data.append("install_scripts = %r" % cwd)
        self.create_conf_file(data)
        super(MyDistribution, self).run_commands()

    def get_conf_filename (self, directory):
        """Get name for config file."""
        return os.path.join(directory, "_%s_configdata.py" % self.get_name())

    def create_conf_file (self, data, directory=None):
        """Create local config file from given data (list of lines) in
        the directory (or current directory if not given)."""
        data.insert(0, "# this file is automatically created by setup.py")
        data.insert(0, "# -*- coding: iso-8859-1 -*-")
        if directory is None:
            directory = os.getcwd()
        filename = self.get_conf_filename(directory)
        # add metadata
        metanames = ("name", "version", "author", "author_email",
                     "maintainer", "maintainer_email", "url",
                     "license", "description", "long_description",
                     "keywords", "platforms", "fullname", "contact",
                     "contact_email")
        for name in metanames:
            method = "get_" + name
            val = getattr(self.metadata, method)()
            data.append("%s = %r" % (name, val))
        data.append('release_date = "%s"' % get_release_date())
        # write the config file
        util.execute(write_file, (filename, data),
                     "creating %s" % filename, self.verbose >= 1, self.dry_run)


class InnoScript:
    """Class to generate INNO script."""

    def __init__(self, lib_dir, dist_dir, windows_exe_files=[],
                 console_exe_files=[], service_exe_files=[],
                 comserver_files=[], lib_files=[]):
        """Store INNO script infos."""
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = AppName
        self.version = AppVersion
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.console_exe_files = [self.chop(p) for p in console_exe_files]
        self.service_exe_files = [self.chop(p) for p in service_exe_files]
        self.comserver_files = [self.chop(p) for p in comserver_files]
        self.lib_files = [self.chop(p) for p in lib_files]
        self.icon = os.path.abspath(r'doc\icon\favicon.ico')

    def chop(self, pathname):
        """Remove distribution directory from path name."""
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]

    def create(self, pathname=r"dist\omt.iss"):
        """Create Inno script."""
        self.pathname = pathname
        self.distfilebase = "%s-%s" % (self.name, self.version)
        self.distfile = self.distfilebase + ".exe"
        with open(self.pathname, "w") as fd:
            self.write_inno_script(fd)

    def write_inno_script (self, fd):
        """Write Inno script contents."""
        print("; WARNING: This script has been created by py2exe. Changes to this script", file=fd)
        print("; will be overwritten the next time py2exe is run!", file=fd)
        print("[Setup]", file=fd)
        print("AppName=%s" % self.name, file=fd)
        print("AppVerName=%s %s" % (self.name, self.version), file=fd)
        print("ChangesEnvironment=true", file=fd)
        print(r"DefaultDirName={pf}\%s" % self.name, file=fd)
        print("DefaultGroupName=%s" % self.name, file=fd)
        print("OutputBaseFilename=%s" % self.distfilebase, file=fd)
        print("OutputDir=..", file=fd)
        print("SetupIconFile=%s" % self.icon, file=fd)
        print(file=fd)
        print("[Tasks]", file=fd)
        print("Name: modifypath; Description: Add application directory to %PATH%;", file=fd)
        print(file=fd)
        # List of source files
        files = self.windows_exe_files + \
                self.console_exe_files + \
                self.service_exe_files + \
                self.comserver_files + \
                self.lib_files
        print('[Files]', file=fd)
        for path in files:
            print(r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path)), file=fd)
        # Set icon filename
        print('[Icons]', file=fd)
        for path in self.windows_exe_files:
            print(r'Name: "{group}\%s"; Filename: "{app}\%s"' %
                  (self.name, path), file=fd)
        for path in self.console_exe_files:
            name = os.path.basename(path).capitalize()
            print(r'Name: "{group}\%s help"; Filename: "cmd.exe"; Parameters: "/K %s --help";' % (name, path), file=fd)
        print(r'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name, file=fd)
        print(file=fd)
        # Uninstall optional log files
        print('[UninstallDelete]', file=fd)
        for path in (self.windows_exe_files + self.console_exe_files):
            exename = os.path.basename(path)
            print(r'Type: files; Name: "{pf}\%s\%s.log"' % (self.name, exename), file=fd)
        print(file=fd)
        # Add app dir to PATH
        print("[Code]", file=fd)
        print("""\
const
    ModPathName = 'modifypath';
    ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
    setArrayLength(Result, 1)
    Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"
""", file=fd)
        shutil.copy(r"scripts\modpath.iss", "dist")


    def compile (self):
        """Compile Inno script with iscc.exe."""
        progpath = get_nt_platform_vars()[0]
        cmd = r'%s\Inno Setup 5\iscc.exe' % progpath
        subprocess.check_call([cmd, self.pathname])

    def sign (self):
        """Sign InnoSetup installer with local self-signed certificate."""
        print("*** signing the inno setup installer ***")
        pfxfile = r'scripts\%s.pfx' % self.lname
        if os.path.isfile(pfxfile):
            path = get_windows_sdk_path()
            signtool = os.path.join(path, "bin", "signtool.exe")
            if os.path.isfile(signtool):
                cmd = [signtool, 'sign', '/f', pfxfile, self.distfile]
                subprocess.check_call(cmd)
            else:
                print("No signed installer: signtool.exe not found.")
        else:
            print("No signed installer: certificate %s not found." % pfxfile)

def get_windows_sdk_path():
    """Return path of Microsoft Windows SDK installation, or None if
    not found."""
    try:
        import _winreg as winreg
    except ImportError:
        import winreg
    sub_key = r"Software\Microsoft\Microsoft SDKs\Windows"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key) as key:
        name = "CurrentInstallFolder"
        return winreg.QueryValueEx(key, name)[0]
    return None

try:
    from py2exe.build_exe import py2exe as py2exe_build

    class MyPy2exe (py2exe_build):
        """First builds the exe file(s), then creates a Windows installer.
        Needs InnoSetup to be installed."""

        def run (self):
            """Generate py2exe installer."""
            # First, let py2exe do it's work.
            py2exe_build.run(self)
            print("*** preparing the inno setup script ***")
            lib_dir = self.lib_dir
            dist_dir = self.dist_dir
            # create the Installer, using the files py2exe has created.
            script = InnoScript(lib_dir, dist_dir, self.windows_exe_files,
                self.console_exe_files, self.service_exe_files,
                self.comserver_files, self.lib_files)
            print("*** creating the inno setup script ***")
            script.create()
            print("*** compiling the inno setup script ***")
            script.compile()
            script.sign()
except ImportError:
    class MyPy2exe:
        """Dummy py2exe class."""
        pass


args = dict(
    name = AppName,
    version = AppVersion,
    description = "portable archive file manager",
    long_description = """Various archive formats can be created, extracted, tested, listed,
searched, compared and repacked by patool. The advantage of patool
is its simplicity in handling archive files without having to remember
a myriad of programs and options.

The archive format is determined by the file(1) program and as a
fallback by the archive file extension.

patool supports 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz), APE (.ape),
AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2),
CAB (.cab), COMPRESS (.Z), CPIO (.cpio),
DEB (.deb), DMS (.dms), FLAC (.flac), GZIP (.gz), ISO (.iso), LRZIP (.lrz),
LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm),
RAR (.rar), RZIP (.rz), SHN (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar)
and ZOO (.zoo) formats.
It relies on helper applications to handle those archive formats
(for example bzip2 for BZIP2 archives).

The archive formats TAR, ZIP, BZIP2 and GZIP
are supported natively and do not require helper applications to be
installed.
""",
    author = MyName,
    author_email = MyEmail,
    maintainer = MyName,
    maintainer_email = MyEmail,
    license = "GPL",
    url = "http://wummel.github.io/patool/",
    packages = ['patoolib', 'patoolib.programs'],
    data_files = data_files,
    scripts = ['patool'],
    keywords = "archiver,archive,compression,commandline,manager",
    classifiers = [
        'Environment :: Console',
        'Topic :: System :: Archiving',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    distclass = MyDistribution,
    cmdclass = {
        'install_lib': MyInstallLib,
        'py2exe': MyPy2exe,
    },
    options = {
        "py2exe": py2exe_options,
        "build_exe": cxfreeze_options,
    },
)
if executables:
    args["executables"] = executables
setup(**args)
