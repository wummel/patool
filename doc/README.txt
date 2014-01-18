Patool
=======

Patool is an archive file manager.

Various archive formats can be  created,  extracted,  tested, listed,
searched, repacked and compared with patool. The advantage of patool is its simplicity in
handling archive files without having to remember a  myriad  of
programs and options.

The  archive format is determined by the file(1) program and as
a fallback by the archive file extension.

patool supports 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz),
APE  (.ape), AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2),
CAB (.cab), COMPRESS (.Z), CPIO (.cpio), DEB  (.deb),  DMS  (.dms),
FLAC  (.flac), GZIP (.gz), ISO (.iso), LRZIP (.lrz), LZH (.lha, .lzh),
LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar),
RZIP (.rz),  SHN  (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar) and
ZOO (.zoo) formats.  It relies on helper applications to handle
those archive formats (for example bzip2 for BZIP2 archives).

The  archive  formats  TAR, ZIP, BZIP2 and GZIP
are supported natively and  do  not  require  helper
applications to be installed.

Examples
---------
```
patool extract archive.zip otherarchive.rar
patool test --verbose dist.tar.gz
patool list package.deb
patool create --verbose /path/to/myfiles.zip file1.txt dir/
patool diff release1.0.tar.gz release2.0.zip
patool search "def urlopen" python-3.3.tar.gz
patool repack linux-2.6.33.tar.gz linux-2.6.33.tar.bz2
```

Website
--------
See http://wummel.github.io/patool/ for more info and downloads.

API
----
You can use patool functions from other Python applications.
Log output will be on sys.stdout and sys.stderr.
On errors, `PatoolError` will be raised.
Note that extra options such as password input or customization
for specific archive programs are not supported.

```
import patoolib
patoolib.extract_archive("archive.zip", outdir="/tmp")
patoolib.test_archive("dist.tar.gz", verbosity=1)
patoolib.list_archive("package.deb")
patoolib.create_archive("/path/to/myfiles.zip", ("file1.txt", "dir/"))
patoolib.diff_archives("release1.0.tar.gz", "release2.0.zip")
patoolib.search_archive("def urlopen", "python3.3.tar.gz")
patoolib.repack_archive("linux-2.6.33.tar.gz", "linux-2.6.33.tar.bz2")
```

Test suite status
------------------
Patool has extensive unit tests to ensure the code quality.
[Travis CI](https://travis-ci.org/) is used for continuous build
and test integration.

[![Build Status](https://travis-ci.org/wummel/patool.png)](https://travis-ci.org/wummel/patool)
