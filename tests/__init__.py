# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Bastian Kleineidam
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
import sys
import patoolib
import pytest
import importlib

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')
patool_cmd = os.path.join(os.path.dirname(basedir), "patool")

# Python 3.x renamed the function name attribute
if sys.version_info[0] > 2:
    fnameattr = '__name__'
else:
    fnameattr = 'func_name'

def _need_func(testfunc, name, description):
    """Decorator skipping test if given testfunc returns False."""
    def check_func(func):
        def newfunc(*args, **kwargs):
            if not testfunc(name):
                raise pytest.skip("%s %r is not available" % (description, name))
            return func(*args, **kwargs)
        setattr(newfunc, fnameattr, getattr(func, fnameattr))
        return newfunc
    return check_func


def needs_os(name):
    """Decorator skipping test if given operating system is not available."""
    return _need_func(lambda x: os.name == x, name, 'operating system')


def needs_program(name):
    """Decorator skipping test if given program is not available."""
    return _need_func(lambda x: patoolib.util.find_program(x), name, 'program')


def needs_one_program(programs):
    """Decorator skipping test if not one of given programs are available."""
    return _need_func(lambda x: all(map(patoolib.util.find_program, x)), programs, 'programs')


def needs_module(name):
    """Decorator skipping test if given module is not available."""
    def has_module(module):
        try:
            importlib.import_module(module)
            return True
        except ImportError:
            return False
    return _need_func(has_module, name, 'Python module')


def needs_codec (program, codec):
    """Decorator skipping test if given program codec is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not patoolib.util.find_program(program):
                raise pytest.skip("program `%s' not available" % program)
            if not has_codec(program, codec):
                raise pytest.skip("codec `%s' for program `%s' not available" % (codec, program))
            return f(*args, **kwargs)
        setattr(newfunc, fnameattr, getattr(f, fnameattr))
        return newfunc
    return check_prog


def has_codec (program, codec):
    """Test if program supports given codec."""
    if program == '7z' and codec == 'rar':
        return patoolib.util.p7zip_supports_rar()
    if patoolib.program_supports_compression(program, codec):
        return True
    return patoolib.util.find_program(codec)


def skip_on_travis():
    """Skip test if TRAVIS build environment is detected."""
    def check_func(func):
        def newfunc(*args, **kwargs):
            if "TRAVIS" in os.environ:
                raise pytest.skip("Skip on TRAVIS CI build.")
            return func(*args, **kwargs)
        setattr(newfunc, fnameattr, getattr(func, fnameattr))
        return newfunc
    return check_func
