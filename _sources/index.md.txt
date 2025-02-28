Patool
=======

Patool is a portable archive file manager for the command line.

Introduction
-------------
[![XKCD Tar comic](https://imgs.xkcd.com/comics/tar.png)](https://xkcd.com/1168/)

I could never remember the correct options for all those different compression
programs. Tar, unzip, gzip - you name it and I forgot it.
Patool remembers all those options for me now so I don't have to.

Description
------------
Various archive types can be  created,  extracted,  tested, listed,
compared, searched  and
repacked with patool. The advantage of patool is its simplicity in
handling archive files without having to remember a  myriad  of
programs and options.

The  archive format is determined by the file(1) program and as
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

The archive formats BZIP2, GZIP, TAR, XZ and ZIP are  supported
natively  and  do  not  require  helper  applications to be
installed.

Installation
-------------
The easy way with pip:

```bash
sudo pip install patool
```

And on Windows:

```bash
py.exe -m pip install patool
```

You will need Python 3.10 or later.

For more information, especially for installing additional tools on Windows, read the detailed
[installation instructions](https://github.com/wummel/patool/blob/master/doc/install.md).


Running
--------
After installation there should be a ```/usr/bin/patool``` binary under Unix
systems, under Windows should exist a file ```c:\python3\scripts\patool```.

Use ```patool``` to run for Linux or OSX systems,  on Windows use
```c:\python3\python3.exe c:\python3\scripts\patool```.

See the following chapter for usage examples.

Examples
---------

```bash
# extract two archives
patool extract archive.zip otherarchive.rar

# test if archive is intact
patool test --verbose dist.tar.gz

# list files inside an archive
patool list package.deb

# create a new archive
patool create --verbose myfiles.zip file1.txt dir/

# list differences between two archive contents
patool diff release1.0.tar.gz release2.0.zip

# search archive contents
patool search "def urlopen" python-3.3.tar.gz

# compress the archive in a different format
patool repack linux-2.6.33.tar.gz linux-2.6.33.tar.bz2
```

Donate
-------
If you like patool, consider a donation to support it. Thanks!

<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="hosted_button_id" value="C5UB3PQF9T33J" />
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
</form>

API
----
If you install patool, there is also a Python module patoolib.
You can use functions in patoolib from other Python applications
to handle archives.

Log output will be on sys.stdout and sys.stderr.
On errors, `PatoolError` will be raised.
Note that extra options or customization for specific archive programs are not supported.

The following functions are currently supported as an API:

```{eval-rst}
.. autofunction:: patoolib.list_formats

.. autofunction:: patoolib.supported_formats

.. autofunction:: patoolib.list_archive

.. autofunction:: patoolib.extract_archive

.. autofunction:: patoolib.test_archive

.. autofunction:: patoolib.create_archive

.. autofunction:: patoolib.diff_archives

.. autofunction:: patoolib.search_archive

.. autofunction:: patoolib.repack_archive

.. autofunction:: patoolib.is_archive
```
