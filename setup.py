# Copyright (C) 2010-2016 Bastian Kleineidam
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
import setuptools

args = dict(
    name = "patool",
    version = "1.12",
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
RAR (.rar), RZIP (.rz), SHN (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar),
ZOO (.zoo) and ZPAQ (.zpaq) formats.
It relies on helper applications to handle those archive formats
(for example bzip2 for BZIP2 archives).

The archive formats TAR, ZIP, BZIP2 and GZIP
are supported natively and do not require helper applications to be
installed.
""",
    author = "Bastian Kleineidam",
    author_email = "bastian.kleineidam@web.de",
    maintainer = "Bastian Kleineidam",
    maintainer_email = "bastian.kleineidam@web.de",
    license = "GPL",
    url = "http://wummel.github.io/patool/",
    keywords = "archiver,archive,compression,commandline,manager",
    classifiers = [
        'Environment :: Console',
        'Topic :: System :: Archiving',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'importlib-metadata ~= 1.0 ; python_version < "3.8"',
    ],
    #packages = ['patoolib', 'patoolib.programs'],
    packages = setuptools.find_packages(),
    entry_points = {'console_scripts': ['patool = patool.patool:main']},
    python_requires=">=3.5",
)

setuptools.setup(**args)
