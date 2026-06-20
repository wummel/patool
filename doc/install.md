Installation
============

First, install the required software.

1. Python >= 3.12 from https://www.python.org/


Now install the application.

1. Installation with pip

   If you have pip installed, run ``pip install patool``.
   To install pip, run ``python -m ensurepip``.

2. Installation on Linux

   Several Linux distributions have packaged patool, for example
   [Debian](https://packages.debian.org/patool),
   [Arch](https://aur.archlinux.org/packages/patool) or
   [Fedora](https://packages.fedoraproject.org/pkgs/patool/patool/).

   Look at the installation instructions for the patool package of
   your distribution.
   But you can also use the pip installation above.

3. Installation on Windows

   See installation with pip above.

   On Windows systems, the archive type is only detectable through file extensions.
   To be able to detect archives with missing or non-standard file extensions,
   you have to install the `file` package from [cygwin](https://cygwin.com/).

   For `patool search`, the `grep` program is needed.
   For `patool diff`, the `diff` program is needed.

   a) Download the [cygwin installer setup-x86_64.exe](https://cygwin.com/setup-x86_64.exe)

   b) Run `setup-x86_64.exe -q -p file,grep,diff`

   c) Add `c:\cygwin64\bin` directory to your PATH

4. Installation in MacOS

   See installation with pip above.
   There is not yet a homebrew formula for patool that I know of.


Suggested archive programs
---------------------------

Installing the following programs lets patool support a wide variety
of archive formats.

[7-zip](https://www.7-zip.org/) supports a lot of formats, installing
it is often sufficient for most users.

[Peazip](https://peazip.github.io/) also supports a lot of
archive formats.

To handle RAR files install either peazip or the
[7zip-rar](https://packages.debian.org/trixie/7zip-rar) package.

For more unusual formats (eg. bzip3) see the ArchivePrograms configuration
at
[patoolib/__init__.py](https://github.com/wummel/patool/blob/3255e723f2bb88f8d4ee43d384b4a05131664991/patoolib/__init__.py#L164).
For each archive format the programs that support extracting,
listing or creating archive files are listed.
