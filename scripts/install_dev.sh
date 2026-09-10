#!/bin/bash
#
# Description: set up a development environment ready for developing this software
#  Package installation uses apt-get which requires sudo permissions
# Requirements:
# - a Debian-based Linux system and sudo permissions for the current user
# - the python-devenv.sh script in your $PATH
# Synopsis: scripts/install_dev.sh

#### shell settings
# abort when using unknown variables
set -o nounset
# abort on subprogram errors
set -o errexit
# abort on piping errors (ie. a|b, a fails)
set -o pipefail
# subshells should inherit error handlers/traps (set -E)
set -o errtrace
# for debugging: print every command with TRACE=1
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# command substitution inherits the errexit setting
shopt -s inherit_errexit
# do not print file globbing patters when no file exists
shopt -s nullglob

#### configuration variables
# the directory this script is stored
BASEDIR=$(realpath "$(dirname "${0}")")
# the project directory
PROJECTDIR=$(dirname "${BASEDIR}")

#### helper functions

# Install a debian package
install_package() {
  local pkg=$1
  if ! dpkg --status "${pkg}" > /dev/null 2>&1; then
    echo "Installing ${pkg}"
    sudo apt-get install \
      --assume-yes \
      --no-install-recommends \
      "${pkg}"
  fi
}

#### main function

# execute make targets
install_package make
# download tool
install_package curl
# augment the local environment
install_package direnv
# lint shell
install_package shellcheck
# for formatting shell scripts (used by make reformat)
install_package shfmt
# install archive handling packages for running tests locally
for pkg in arc archmage arj binutils bzip2 cabextract lzip lz4 plzip clzip pdlzip \
           cpio flac genisoimage lbzip2 libarchive-tools lhasa lrzip lzop ncompress \
           nomarch pbzip2 7zip 7zip-standalone 7zip-rar rpm2cpio unzip unace unalz \
           unar sharutils tar xdms zip zopfli zpaq zpaqfranz zstd; do
  install_package "$pkg"
done

# the rest of this scripts relies on being in the project directory
cd "${PROJECTDIR}"

# initialize the dev env with uv
python-devenv.sh
