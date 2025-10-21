Development with the patoolib library
======================================

The patool functionality can also be used in other Python programs.
To do this, install the patool program, import the library and
use one or more of the convenience functions.

import patoolib
try:
    patoolib.extract("myarchive.zip", verbose=True)
    print("Success.")
except patoolib.util.PatoolError as msg:
    print("Error:", msg)

General rules for all convenience functions:

* All convenience functions raise PatoolError on errors.

* If your application is not interactive, you should set ``interactive=False``.
  Otherwise the function call could block while it waits for user input.

* Error messages are printed on stderr, informative messages
  are printed on stdout.

* All file arguments are filenames. File objects are not accepted
  as input.

* Filenames can be relative or absolute.

* If verbosity is increased, additional output of the archive
  program is shown.

* Usually the program to be executed is automatically determined
  but it can be set manually with the program parameter.

The convenience functions are:

* ``def extract_archive(archive, verbosity=0, outdir=None, program=None, interactive=True, password=None)``

  Extracts the given archive filename to the current working directory
  or if specified to the given directory name in outdir.
  Checks that the archive exists and is readable before extracting it.

* ``def list_archive(archive, verbosity=1, program=None, interactive=True, password=None)``

  Lists the contents of the given archive filename on stdout.
  Checks that the archive exists and is readable before listing it.

* ``def test_archive(archive, verbosity=0, program=None, interactive=True, password=None)``

  Tests the given archive filename.
  Checks that the archive exists and is readable before testing it.

* ``def create_archive(archive, filenames, verbosity=0, program=None, interactive=True, password=None)``

  Creates a new archive. The type of archive is determined
  by the archive filename extension.
  Checks that the archive is not already existing to avoid overwriting it.
  Also checks that the filename list is not empty and that all files exist
  and are readable.

* ``diff_archives(archive1, archive2, verbosity=0, interactive=True)``

  This function lists differences in the content of the two archives.
  Both archives are extracted and the contents are compared
  recursively with the diff(1) program.
  Checks that both archives exist and are readable.

* ``def search_archive(pattern, archive, verbosity=0, interactive=True, password=None)``

  This function searches the given pattern in the archive file contents
  with grep(1).
  Checks that archive exists and is readable.

* ``repack_archive (archive, archive_new, verbosity=0, interactive=True, password=None)``

  This function extracts the contents of the archive and packs them
  into archive_new.
  Checks that archive exists and is readable. Also checks that
  archive_new does not exist to avoid overwriting it.
