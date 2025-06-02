Development
============

Development for patool needs the following environment:

1. Debian Linux or a similar distribution like Ubuntu

2. GNU make

3. A user with sudo permissions.


To start developing, run the following commands:

1. Checkout the source code and change into base project directory

   $ git clone https://github.com/wummel/patool.git && cd patool

2. Initialize the source directory

   $ scripts/install_dev.sh
   $ make init

   This installs required packages, creates a virtual Python environment in the directory `.venv/`
   and installs required modules for development.

3. Run the tests

   $ make test

4. Change the code, and test the new code by running the tests again


The Github workflow runs tests on different architectures and Python versions.
Currently, tests are run on Windows, MacOS and Linux.
Tested Python versions are Python 3.11, 3.12 and 3.13.
