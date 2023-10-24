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
"""
A lot of these tests need an external compression program.
See https://github.com/wummel/patool/blob/debian/debian/control
at the "Suggests:" for a list of packages with supported compression
programs.

The file type detection uses the file(1) program which uses a library
of "magic" patterns. The contents of the magic pattern library can vary
between distributions so the tests might not run on all Linux systems.
"""
import os
import patoolib
import pytest
import importlib

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')

# Python 3.x function name attribute
fnameattr = '__name__'

def _need_func(testfunc, name, description):
    """Decorator skipping test if given testfunc returns False."""
    def check_func(func):
        def newfunc(*args, **kwargs):
            if not testfunc(name):
                pytest.skip("%s %r is not available" % (description, name))
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
    return _need_func(lambda x: any(map(patoolib.util.find_program, x)), programs, 'programs')


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
                pytest.skip("program `%s' not available" % program)
            if not has_codec(program, codec):
                pytest.skip("codec `%s' for program `%s' not available" % (codec, program))
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
