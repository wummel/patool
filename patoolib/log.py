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
"""Logging functions."""
import os
import sys
import time
import logging
from . import configuration


# the global logging.Logger object, initialized by init_logging()
logger = None


def init_logging(stream=sys.stderr):
    """Initialize the global logger. All log messages will be
    sent to the given stream, default is sys.stderr.
    """
    global logger
    logger = logging.getLogger(configuration.AppName)
    handler = logging.StreamHandler(stream=stream)
    format = f"%(levelname)s {configuration.AppName}: %(message)s"
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def encode_safe(*args, encoding=sys.stderr.encoding):
    """Replacing unknown characters in args for the given encoding.
    @return: a space-separated string that will not have encoding errors
    with the given encoding
    """
    return " ".join(
        [str(arg).encode(encoding, errors="replace").decode() for arg in args]
    )


def log_error(msg):
    """Log error message."""
    logger.error(encode_safe(msg))


def log_warning(msg):
    """Log warning message."""
    logger.warning(encode_safe(msg))


def log_info(msg):
    """Log info message."""
    logger.info(encode_safe(msg))


# environment keys to print for internal error info
EnvKeys = ("LANGUAGE", "LC_ALL", "LC_CTYPE", "LANG")


def log_internal_error():
    """Print internal error message."""
    now = strtime(time.time())
    env = os.linesep.join(
        [f"{key}={os.getenv(key)!r}" for key in EnvKeys if os.getenv(key) is not None]
    )
    logger.exception(
        encode_safe(
            f"""********** Oops, I did it again. *************

You have found an internal error in {configuration.AppName}.
Please write a bug report at
{configuration.SupportUrl}
and include at least the information below:

Not disclosing some of the information below due to privacy reasons is ok.
I will try to help you nonetheless, but you have to give me something
I can work with ;) .

{configuration.App}
Python {sys.version} on {sys.platform}
Local time: {now}
sys.orig_argv: {sys.orig_argv}
Environment:
{env}
******** {configuration.AppName} internal error, over and out ********
"""
        )
    )


def strtime(t):
    """Return ISO 8601 formatted time."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + strtimezone()


def strtimezone():
    """Return timezone info, %z on some platforms, but not supported on all."""
    if time.daylight:
        zone = time.altzone
    else:
        zone = time.timezone
    return "%+04d" % (-zone // 3600)


init_logging()
