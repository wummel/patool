#!/bin/bash
#
# Description: set up a development environment ready for developing this software
#  Package installation uses apt-get which requires sudo permissions
# Requirements: a Debian-based Linux system and sudo permissions for the current user
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

PY_VER=$(grep "python_version_dev =" "${PROJECTDIR}/pyproject.toml" | cut -f2 -d'"')
UV_VER=$(grep "uv_version_dev =" "${PROJECTDIR}/pyproject.toml" | cut -f2 -d'"')
DOWNLOAD_URL_UV=https://github.com/astral-sh/uv/releases/download/${UV_VER}/uv-x86_64-unknown-linux-gnu.tar.gz
CURL_OPTS=("--location" "--silent" "--show-error" "--retry" "2" "--fail")
REINSTALL_PYTHON=0


#### helper functions

# Install a debian package
install_package() {
  local pkg=$1
  if ! dpkg --status "${pkg}" >/dev/null 2>&1; then
    echo "Installing ${pkg}"
    sudo apt-get install "${pkg}"
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
# install archive handling packages for running tests locally
# note: 7zip, 7zip-standalone and 7zip-rar are currently only available in bookworm-backports
# add the following line to /etc/apt/sources.list make them available:
# deb http://deb.debian.org/debian/ bookworm-backports main non-free-firmware non-free contrib
for pkg in arc archmage arj binutils bzip2 cabextract lzip lz4 plzip clzip pdlzip \
           cpio flac genisoimage lbzip2 libarchive-tools lhasa lrzip lzop ncompress \
           nomarch pbzip2 7zip 7zip-standalone 7zip-rar rpm2cpio unzip unace unalz \
           unar sharutils tar xdms zip zopfli zstd; do \
  # ignore errors, since 7zip packages are only available from backported repositories
  install_package "$pkg" || true
done

# the rest of this scripts relies on being in the project directory
cd "${PROJECTDIR}"

# install uv
if [ ! -d bin ]; then
    mkdir bin
fi
if [ ! -f bin/uv ]; then
    echo "Install uv ${UV_VER} from ${DOWNLOAD_URL_UV}"
    (cd bin; curl "${CURL_OPTS[@]}" "${DOWNLOAD_URL_UV}" | tar xzv --strip-components 1)
elif [ "$(bin/uv version | cut -d" " -f2)" != "${UV_VER}" ]; then
    echo "Updating $(bin/uv version) to ${UV_VER} from ${DOWNLOAD_URL_UV}"
    (cd bin; curl "${CURL_OPTS[@]}" "${DOWNLOAD_URL_UV}" | tar xzv --strip-components 1)
    REINSTALL_PYTHON=1
fi

# add local development environment for direnv
if ! declare -F _direnv_hook >/dev/null; then
    eval "$(direnv hook bash)"
fi
if [ ! -f .envrc ]; then
    (
    echo "# to find local tools"
    echo "export PATH=${PROJECTDIR}/bin\${PATH:+:\$PATH}"
    echo "export PATH=${PROJECTDIR}/.venv/bin\${PATH:+:\$PATH}"
    ) > .envrc
    direnv allow .
    source .envrc
fi

# create .python-version
if [ ! -f .python-version ]; then
  echo "Generating $PROJECTDIR/.python-version"
  echo "${PY_VER}" > .python-version
else
  PROJ_PY_VER=$(<.python-version)
  if [ ".$PROJ_PY_VER" != ".$PY_VER" ]; then
    echo "Updating $PROJECTDIR/.python-version (${PROJ_PY_VER} -> ${PY_VER})"
    echo "${PY_VER}" >| .python-version
    rm -rf .venv
  fi
fi

# create virtual environment
if [ ! -d .venv ]; then
    uv venv
fi

if [ "{REINSTALL_PYTHON}"=1 ]; then
    uv python install --reinstall
fi
