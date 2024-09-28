Development
============

Development for patool needs the following environment:

1. Python >= 3.10 from https://www.python.org/

2. uv from https://github.com/astral-sh/uv

   Install the `uv` binary into a local directory in your PATH.

3. GNU make


To start developing, run the following commands:

1. Checkout the source code and change into base project directory

   $ git clone https://github.com/wummel/patool.git && cd patool

2. Initialize the source directory

   $ make init

   This creates a virtual Python environment in the directory `.venv/` and installs
   required modules for development.

   You should add the virtual Python environment binaries to PATH

   $ export PATH=.venv/bin:$PATH

3. Run the tests

   $ make test

4. Change the code, and test the new code by installing patool in the virtual Python environment

   $ make localbuild

   Now the `patool` binary will be installed in the `.venv/bin` directory.

