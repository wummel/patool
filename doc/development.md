Development
============

Development for patool is done with the following environment:

1. Debian Linux or a similar distribution like Ubuntu

2. A user with sudo permissions to install required system packages.


To start developing, run the following commands:

1. Checkout the source code and change into base project directory

   `git clone https://github.com/wummel/patool.git && cd patool`

2. Initialize the source directory and install system packages

   `scripts/install_dev.sh`

   This script installs required system packages and a lot of archive programs for testing
   with `sudo apt-get install <package>`.
   It also downloads the uv tool to `./bin/uv` and configures the PATH variable in `.envrc`
   for `direnv` to find it.

3. Create the Python virtual environment

   `make init`

   This command creates a virtual Python environment in the directory `.venv/`
   and installs required Python modules for development with `uv`.
   Rerun this when changing dependencies in pyproject.toml

3. Run the tests

   `make test`

   This runs all tests in parallel. Tests detect necessary features and programs to run,
   so they do not fail but are skipped when archive programs are missing.

4. Now change the code, eg. to implement a new features.
   After changing the code you should run the following commands:

   `make lint`

   This catches simple coding and syntax errors. Run this first after changing the code.

   `make test`

   Run the tests again with the changed code. It is a good idea to add new tests when
   adding new features.

   `make reformat`

   Formats the code according to the configured rules in .ruff.toml.
   Run this before git commit.

5. Other make targets are documented in the Makefile itself.
   Use this command to display all make targets with a short explanation:

   `make help`



After committing and pushing new code to a github repository, the Github workflow defined
in `.github/workflows/python-package.yml` runs.
The python-package.yml workflow tests different architectures and Python versions.
Tests are run on Windows, MacOS and Linux, tested Python versions are Python 3.12, 3.13 and 3.14.

A useful tool to test your github workflow on a local system is https://github.com/nektos/act,
though it only supports Linux systems.
