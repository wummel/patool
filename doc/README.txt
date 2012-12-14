Patool
=======

Various archive types can be  created,  extracted,  tested  and
listed with patool. The advantage of patool is its simplicity in
handling archive files without having to remember a  myriad  of
programs and options.

The  archive format is determined by the file(1) program and as
a fallback by the archive file extension.

patool supports 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz),
APE  (.ape), AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2), CAB
(.cab), compress (.Z), CPIO (.cpio), DEB  (.deb),  DMS  (.dms),
FLAC  (.flac), GZIP (.gz), LRZIP (.lrz), LZH (.lha, .lzh), LZIP
(.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar),  RZIP
(.rz),  SHN  (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar) and
ZOO (.zoo) formats.  It relies on helper applications to handle
those archive formats (for example bzip2 for BZIP2 archives).

The  archive  formats  TAR (.tar), ZIP (.zip), BZIP2 (.bz2) and
GZIP (.gz) are supported natively and  do  not  require  helper
applications to be installed.

Examples
---------
```
patool extract archive.zip otherarchive.rar
patool test --verbose dist.tar.gz
patool list package.deb
patool create --verbose myfiles.zip file1.txt dir/
patool diff release1.0.tar.gz release2.0.zip
patool repack linux-2.6.33.tar.gz linux-2.6.33.tar.bz2
```

Website
--------
See http://wummel.github.com/patool/ for more info and downloads.

