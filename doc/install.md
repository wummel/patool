Installation
============

First, install the required software.

1. Python >= 3.10 from https://www.python.org/


Now install the application.

1. Installation with pip

   If you have pip installed: ``pip install patool``

2. Installation from source

   a) Installation as root

      Run ``sudo python setup.py install`` to install patool.

   b) Installation as a normal user

      Run ``python setup.py install --home $HOME``. Note that you have
      to adjust your PATH and PYTHONPATH environment variables, e.g. by
      adding the commands ``export PYTHONPATH=$HOME/lib/python`` and
      ``export PATH=$PATH:$HOME/bin`` to your shell configuration
      file.

      For more information look at the
      [Modifying Python's search path](http://docs.python.org/inst/search-path.html#SECTION000410000000000000000)
      documentation.

3. Optional: install cygwin file, grep and diff packages on Windows

   On Windows systems, the archive type is only detectable through file extensions.
   To be able to detect archives with missing or non-standard file extensions,
   you have to install the `file` package from [cygwin](https://cygwin.com/).

   For `patool search`, the `grep` program is needed.
   For `patool diff`, the `diff` program is needed.

   a) Download the [cygwin installer setup-x86_64.exe](https://cygwin.com/setup-x86_64.exe)

   b) Run `setup-x86_64.exe -q -p file,grep,diff`

   c) Add the `c:\cygwin64\bin` directory to your PATH


After installation
------------------
Patool is now installed. Have fun!
