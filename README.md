Patool
=======

Patool is an archive file manager.

Various archive formats can be created, extracted, tested, listed,
searched, repacked and compared with patool. The advantage of patool is
its simplicity in handling archive files without having to remember a
myriad of programs and options.

The archive format is determined by the file(1) program and as
a fallback by the archive file extension.

patool supports 7z (.7z, .cb7), ACE (.ace, .cba), ADF (.adf), ALZIP (.alz),
APE (.ape), AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2), BZIP3 (.bz3),
CAB (.cab), CHM (.chm), COMPRESS (.Z), CPIO (.cpio), DEB (.deb), DMS (.dms),
FLAC (.flac), GZIP (.gz), ISO (.iso), LRZIP (.lrz), LZH (.lha, .lzh),
LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar, .cbr),
RZIP (.rz), SHN (.shn), TAR (.tar, .cbt), UDF (.udf), XZ (.xz),
ZIP (.zip, .jar, .cbz), ZOO (.zoo) and ZSTANDARD (.zst) archive formats.

It relies on helper applications to handle those archive formats
(for example `xz` for XZ (.xz) archives).

The archive formats TAR, ZIP, BZIP2 and GZIP are supported natively
and do not require helper applications to be installed.

Examples
---------
```
# Extract several archives with different formats
patool extract archive.zip otherarchive.rar

# Extract archive with password
patool extract --password somepassword archive.rar

# Test archive integrity
patool test --verbose dist.tar.gz

# List files stored in an archive
patool list package.deb

# Create a new archive
patool create --verbose /path/to/myfiles.zip file1.txt dir/

# Create a new archive with password
patool create --verbose --password somepassword /path/to/myfiles.zip file1.txt dir/

# Show differences between two archives
patool diff release1.0.tar.gz release2.0.zip

# Search for text inside archives
patool search "def urlopen" python-3.3.tar.gz

# Repackage an archive in a different format
patool repack linux-2.6.33.tar.gz linux-2.6.33.tar.bz2
```

Website
--------
See https://wummel.github.io/patool/ for more info and downloads.

API
----
You can use patool functions from other Python applications.
Log output will be on sys.stdout and sys.stderr.
On errors, `PatoolError` will be raised.
Note that extra options or customization
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
patoolib.is_archive("package.deb")
```

See https://wummel.github.io/patool/ for detailed API documentation.

Test suite
-----------
Patool has [extensive unit tests](https://github.com/wummel/patool/tree/master/tests) to ensure the code quality.
The tests are run on each commit by a github runner.


Bash completion
----------------
Install the argcomplete python package with
`apt-get install python3-argcomplete`,
then run
`eval "$(register-python-argcomplete patool)"`.
After that typing `patool`, a `<SPACE>` and then `<TAB>`
lists available options and commands.
