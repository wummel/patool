#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
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
"""
Setup file for the distuils module.
"""
from __future__ import print_function
import sys
if not hasattr(sys, "version_info") or sys.version_info < (2, 7, 0, "final", 0):
    raise SystemExit("This program requires Python 2.7 or later.")
import os
import shutil
import glob
import subprocess
try:
    from cx_Freeze import setup, Executable
except ImportError:
    from distutils.core import setup
from distutils.command.register import register
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
from distutils import util

AppName = "Patool"
AppVersion = "0.18"
MyName = "Bastian Kleineidam"
MyEmail = "calvin@users.sourceforge.net"

py_excludes = ['doctest', 'unittest', 'Tkinter', '_ssl', 'pdb',
  'email', 'calendar', 'ftplib', 'httplib', 'pickle', 'optparse','rfc822'
]
# py2exe options for Windows packaging
py2exe_options = dict(
    packages=["encodings"],
    excludes=py_excludes,
    # silence py2exe error about not finding msvcp90.dll
    dll_excludes=['MSVCP90.dll'],
    compressed=1,
    optimize=2,
)
# cx_Freeze for Linux RPM packaging
cxfreeze_options = dict(
    packages=["encodings"],
    excludes=py_excludes,
)

# Microsoft Visual C++ runtime version (tested with Python 2.7.2)
MSVCP90Version = '9.0.21022.8'
MSVCP90Token = '1fc8b3b9a1e18e3b'


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


class MyDistribution (Distribution, object):
    """Custom distribution class generating config file."""

    def __init__ (self, attrs):
        """Set console and windows scripts."""
        super(MyDistribution, self).__init__(attrs)
        self.console = ['patool']


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
        print(r"DefaultDirName={pf}\%s" % self.name, file=fd)
        print("DefaultGroupName=%s" % self.name, file=fd)
        print("OutputBaseFilename=%s" % self.distfilebase, file=fd)
        print("OutputDir=..", file=fd)
        print("SetupIconFile=%s" % self.icon, file=fd)
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
        print(r'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name, file=fd)
        print(file=fd)
        # Uninstall optional log files
        print('[UninstallDelete]', file=fd)
        print(r'Type: files; Name: "{pf}\%s\patool*.exe.log"' % self.name, file=fd)
        print(file=fd)

    def compile (self):
        """Compile Inno script with iscc.exe."""
        progpath = get_nt_platform_vars()[0]
        cmd = r'%s\Inno Setup 5\iscc.exe' % progpath
        subprocess.check_call([cmd, self.pathname])

    def sign (self):
        """Sign InnoSetup installer with local self-signed certificate."""
        pfxfile = r'C:\patool.pfx'
        if os.path.isfile(pfxfile):
            cmd = ['signtool.exe', 'sign', '/f', pfxfile, self.distfile]
            subprocess.check_call(cmd)
        else:
            print("No signed installer: certificate %s not found." % pfxfile)

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


class MyRegister (register, object):
    """Custom register command."""

    def build_post_data(self, action):
        """Force application name to lower case."""
        data = super(MyRegister, self).build_post_data(action)
        data['name'] = data['name'].lower()
        return data


args = dict(
    name = AppName,
    version = AppVersion,
    description = "portable command line archive file manager",
    long_description = """Various archive types can be created, extracted, tested and listed by
patool. The advantage of patool is its simplicity in handling archive
files without having to remember a myriad of programs and options.

The archive format is determined by the file(1) program and as a
fallback by the archive file extension.

patool supports 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz), APE (.ape),
AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2),
CAB (.cab), compress (.Z), CPIO (.cpio),
DEB (.deb), DMS (.dms), FLAC (.flac), GZIP (.gz), LRZIP (.lrz),
LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm),
RAR (.rar), RZIP (.rz), SHN (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar)
and ZOO (.zoo) formats.
It relies on helper applications to handle those archive formats
(for example bzip2 for BZIP2 archives).

The archive formats TAR (.tar), ZIP (.zip), BZIP2 (.bz2) and GZIP (.gz)
are supported natively and do not require helper applications to be
installed.
""",
    author = MyName,
    author_email = MyEmail,
    maintainer = MyName,
    maintainer_email = MyEmail,
    license = "GPL",
    url = "http://wummel.github.com/patool/",
    download_url="http://wummel.github.com/patool/files/",
    packages = ['patoolib', 'patoolib.programs'],
    data_files = data_files,
    scripts = ['patool'],
    keywords = "archiver,compression,commandline",
    classifiers = [
        'Environment :: Console',
        'Topic :: System :: Archiving',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    distclass = MyDistribution,
    cmdclass = {
        'py2exe': MyPy2exe,
        'register': MyRegister,
    },
    options = {
        "py2exe": py2exe_options,
        "build_exe": cxfreeze_options,
    },
)
if executables:
    args["executables"] = executables
setup(**args)
