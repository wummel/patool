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
"""Utility functions."""
import os
import sys
import shutil
import subprocess
from .log import log_info


class PatoolError(Exception):
    """Raised when errors occur."""
    pass


class memoized:
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """

    def __init__(self, func):
        """Set func and init cache."""
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        """Try to find result for function arguments in local cache or
        execute the function and fill the cache with the result.
        """
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


def backtick(cmd, encoding='utf-8'):
    """Return decoded output from command."""
    return subprocess.run(cmd, stdout=subprocess.PIPE, check=True,
                          encoding=encoding, errors="replace").stdout


def run_under_pythonw():
    """Return True iff this script is run with pythonw.exe on Windows."""
    return (
        os.name == 'nt' and
        sys.executable is not None and
        sys.executable.lower().endswith('pythonw.exe')
    )


def run(cmd, verbosity=0, **kwargs):
    """Run command without error checking.
    @return: command return code
    """
    # Note that shell_quote_nt() result is not suitable for copy-paste
    # (especially on Unix systems), but it looks nicer than shell_quote().
    if verbosity >= 0:
        info = " ".join(map(shell_quote_nt, cmd))
        log_info(f"running {info}")
    if run_under_pythonw():
        # prevent opening of additional consoles when running with pythonw.exe
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    # try to prevent hangs for programs requiring input
    kwargs["input"] = ""
    if kwargs:
        if verbosity >= 0:
            info = ", ".join(f"{k}={shell_quote(str(v))}" for k, v in kwargs.items())
            log_info(f"    with {info}")
        if kwargs.get("shell"):
            # for shell calls the command must be a string
            cmd = " ".join(cmd)
    if verbosity < 1:
        # hide command output on stdout
        kwargs['stdout'] = subprocess.DEVNULL
    res = subprocess.run(cmd, **kwargs)
    return res.returncode


def run_checked(cmd, ret_ok=(0,), **kwargs):
    """Run command and raise PatoolError on error."""
    retcode = run(cmd, **kwargs)
    if retcode not in ret_ok:
        msg = f"Command `{cmd}' returned non-zero exit status {retcode}"
        raise PatoolError(msg)
    return retcode


def shell_quote(value):
    """Quote all shell metacharacters in given string value with strong
    (i.e. single) quotes, handling the single quote especially.
    """
    if os.name == 'nt':
        return shell_quote_nt(value)
    return shell_quote_unix(value)


def shell_quote_unix(value):
    """Quote argument for Unix system."""
    value = value.replace("'", r"'\''")
    return f"'{value}'"


def shell_quote_nt(value):
    """Quote argument for Windows system. Modeled after distutils
    _nt_quote_args() function.
    """
    if " " in value:
        return f'"{value}"'
    return value


def p7zip_supports_rar():
    """Determine if the RAR codec is installed for 7z program."""
    if os.name == 'nt':
        # Assume RAR support is compiled into the binary.
        return True
    # the subdirectory and codec name
    codecnames = ['p7zip/Codecs/Rar29.so', 'p7zip/Codecs/Rar.so']
    # search canonical user library dirs
    for libdir in ('/usr/lib', '/usr/local/lib', '/usr/lib64', '/usr/local/lib64', '/usr/lib/i386-linux-gnu', '/usr/lib/x86_64-linux-gnu'):
        for codecname in codecnames:
            fname = os.path.join(libdir, codecname)
            if os.path.exists(fname):
                return True
    return False


def system_search_path():
    """Get the list of directories to search for executable programs."""
    path = os.environ.get("PATH", os.defpath)
    if os.name == 'nt':
        # Add some well-known archiver programs to the search path
        path = append_to_path(path, get_nt_7z_dir())
        path = append_to_path(path, get_nt_mac_dir())
        path = append_to_path(path, get_nt_winrar_dir())
    return path


def append_to_path(path, directory):
    """Add a directory to the PATH environment variable, if it is a valid
    directory.
    """
    if not os.path.isdir(directory) or directory in path:
        return path
    if not path.endswith(os.pathsep):
        path += os.pathsep
    return path + directory


@memoized
def find_program(program):
    """Look for given program."""
    return shutil.which(program, path=system_search_path())


def get_nt_7z_dir():
    """Return 7-Zip directory from registry, or an empty string."""
    import winreg
    import platform
    python_bits = platform.architecture()[0]
    keyname = r"SOFTWARE\7-Zip"
    try:
        if python_bits == '32bit' and platform.machine().endswith('64'):
            # get 64-bit registry key from 32-bit Python
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyname,
                  0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        else:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyname)
        try:
            return winreg.QueryValueEx(key, "Path")[0]
        finally:
            winreg.CloseKey(key)
    except OSError:
        return ""


def get_nt_program_dir():
    """Return the Windows program files directory."""
    progvar = "%ProgramFiles%"
    return os.path.expandvars(progvar)


def get_nt_mac_dir():
    """Return Monkey Audio Compressor (MAC) directory."""
    return os.path.join(get_nt_program_dir(), "Monkey's Audio")


def get_nt_winrar_dir():
    """Return WinRAR directory."""
    return os.path.join(get_nt_program_dir(), "WinRAR")


def strlist_with_or(alist):
    """Return comma separated string, and last entry appended with ' or '."""
    if len(alist) > 1:
        head = ", ".join(alist[:-1])
        tail = alist[-1]
        return f"{head} or {tail}"
    return ", ".join(alist)
