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
import patoolib
import pytest

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')


def needs_os (name):
    """Decorator skipping test if given program is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if os.name != name:
                raise pytest.skip("operating system %s not found" % name)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_program (program):
    """Decorator skipping test if given program is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not patoolib.util.find_program(program):
                raise pytest.skip("program `%s' not available" % program)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_one_program (programs):
    """Decorator skipping test if not one of given programs are available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            for program in programs:
                if patoolib.util.find_program(program):
                    break
            else:
                raise pytest.skip("None of programs %s available" % programs)
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def needs_codec (program, codec):
    """Decorator skipping test if given program codec is not available."""
    def check_prog (f):
        def newfunc (*args, **kwargs):
            if not patoolib.util.find_program(program):
                raise pytest.skip("program `%s' not available" % program)
            if not has_codec(program, codec):
                raise pytest.skip("codec `%s' for program `%s' not available" % (codec, program))
            return f(*args, **kwargs)
        newfunc.func_name = f.func_name
        return newfunc
    return check_prog


def has_codec (program, codec):
    """Test if program supports given codec."""
    if program == '7z' and codec == 'rar':
        return patoolib.util.p7zip_supports_rar()
    if patoolib.program_supports_compression(program, codec):
        return True
    return patoolib.util.find_program(codec)


