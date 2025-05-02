# This Makefile is only used by developers.

############# Settings ############
# use Bash as shell, not sh
SHELL := bash
# execute makefile in a single bash process instead of one per target
.ONESHELL:
# set Bash flags
.SHELLFLAGS := -eu -o pipefail -c
# remove target files if a rule fails, forces reruns of aborted rules
.DELETE_ON_ERROR:
# warn for undefined variables
MAKEFLAGS += --warn-undefined-variables
# disable builtin default rules
MAKEFLAGS += --no-builtin-rules


############ Configuration ############
VERSION:=$(shell grep "Version: str =" patoolib/configuration.py | cut -d '"' -f2)
AUTHOR:=$(shell grep "MyName: str =" patoolib/configuration.py | cut -d '"' -f2)
APPNAME:=$(shell grep "AppName: str =" patoolib/configuration.py | cut -d '"' -f2)
ARCHIVE_SOURCE:=$(APPNAME)-$(VERSION).tar.gz
ARCHIVE_WHEEL:=$(APPNAME)-$(VERSION)-py2.py3-none-any.whl
GITRELEASETAG:=$(VERSION)
GITUSER:=wummel
GITREPO:=$(APPNAME)
HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WEBMETA:=doc/web/source/conf.py
CHANGELOG:=doc/changelog.txt
GIT_MAIN_BRANCH:=master
# Pytest options:
# -s: do not capture stdout/stderr (some tests fail otherwise)
# --full-trace: print full stacktrace on keyboard interrupts
# --log-file: write test output to file for easier inspection
# --numprocesses auto: run tests in parallel on available CPU cores (uses pytest-xdist) 
PYTESTOPTS?=-s --full-trace --log-file=build/test.log --numprocesses auto
# which test modules to run
TESTS ?= tests/
# set test options
TESTOPTS=

############ Default target ############

# `make help` displays all targets documented with `##`in the target line
.PHONY: help
help:	## display this help section
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help


############ Installation and provisioning  ############

# these targets work best in a virtual python environment
# see https://github.com/pyenv/pyenv for more info

.PHONY: init ## install python virtual env and required development packages
init:
	uv sync


############ Build and release targets ############

.PHONY: clean
clean: ## remove generated python, web page files and all local patool installations
	python setup.py clean --all
	uv pip uninstall patool
	$(MAKE) -C doc/web clean

.PHONY: distclean
distclean:	clean ## run clean and additionally remove all build and dist files
	rm -rf build dist
	rm -f MANIFEST
# clean aborted dist builds and output files
	rm -rf $(APPNAME)-$(VERSION) $(APPNAME).egg-info
	rm -f *-stamp*

.PHONY: dist
dist: ## build source and wheel distribution file
	uv build

.PHONY: release-pypi
release-pypi: ## upload a new release to pypi
	uv publish dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_WHEEL)

# export GITHUB_TOKEN for the hub command
# Generate a fine grained access token with:
# - Restricted to this repository (patool)
# - Repository permission: Metadata -> Read (displayed as "Read access to metadata" in token view)
# - Repository permission: Contents -> Read and write (displayed as "Read and Write access to code" in token view)
# - Expiration in 90 days
# After that run "export GITHUB_TOKEN=<token-content>"
.PHONY: release-gh
release-gh:	## upload a new release to github
	gh release create \
	  --title "Release $(GITRELEASETAG)" \
	  --notes "See doc/changelog.txt for release notes" \
	  --latest \
	  --draft=false \
	  --prerelease=false \
	  --verify-tag  \
	  "$(GITRELEASETAG)" \
	  dist/$(ARCHIVE_SOURCE) \
	  dist/$(ARCHIVE_WHEEL)


# Make a new release by calling all the distinct steps in the correct order.
# Each step is a separate target so that it's easy to do this manually if
# anything screwed up.
.PHONY: release
release: distclean releasecheck ## release a new version of patool
	$(MAKE) dist release-gh release-pypi release-homepage github-issues

.PHONY: releasecheck
releasecheck: update_webmeta checkgit checkchangelog lint test typecheck checkgitreleasetag ## check that repo is ready for release

.PHONY: checkgit
checkgit: ## check that git changes are all committed on the main branch
# check that branch is the main branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "$(GIT_MAIN_BRANCH)" ]; then \
	  echo "ERROR: current git branch is not '$(GIT_MAIN_BRANCH)'"; \
	  git rev-parse --abbrev-ref HEAD; \
	  false; \
	fi
# check for uncommitted versions
	@if [ -n "$(shell git status --porcelain --untracked-files=all)" ]; then \
	  echo "ERROR: uncommitted git changes"; \
	  git status --porcelain --untracked-files=all; \
	  false; \
	fi

.PHONY: checkgitreleasetag
checkgitreleasetag:	## check release tag for git exists
	@if [ -z "$(shell git tag -l -- $(GITRELEASETAG))" ]; then \
	  echo "ERROR: git tag \"$(GITRELEASETAG)\" does not exist, execute 'git tag -a $(GITRELEASETAG) -m \"$(GITRELEASETAG)\"'"; \
	  false; \
	fi
# check that release tags is pushed to remote
	@if ! git ls-remote --exit-code --tags origin $(GITRELEASETAG); then \
	  echo "ERROR: git tag \"$(GITRELEASETAG)\" does not exist on remote repo, execute 'git push --tags'"; \
	fi

.PHONY: github-issues
github-issues: ## close github issues mentioned in changelog
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	cd .. && github-changelog $(GITUSER) $(GITREPO) patool.git/doc/changelog.txt


############ Versioning ############

bumpversion-%: ## shortcut target for bumpversion: bumpversion-{major,minor,patch}
	bumpversion $*
	$(MAKE) bumpchangelog

bumpchangelog: ## add leading changelog entry for a new version
	sed -i '1i$(VERSION) (released xx.xx.xxxx)\n  *\n' $(CHANGELOG)


checkchangelog: ## check changelog before release
	@if egrep -i "xx\.|xxxx|\.xx" $(CHANGELOG) > /dev/null; then \
	  echo "Could not release: edit $(CHANGELOG) release date"; false; \
	fi
	@if ! grep "^$(VERSION)" $(CHANGELOG) > /dev/null; then \
	  echo "ERROR: Version $(VERSION) missing from $(CHANGELOG)"; \
	  false; \
	fi
	@if ! head -n1 $(CHANGELOG) | egrep "^$(VERSION)" >/dev/null; then \
	  echo "Could not release: different versions in $(CHANGELOG) and setup.py"; \
	  echo "Version in $(CHANGELOG):"; head -n1 $(CHANGELOG); \
	  echo "Version in setup.py: $(VERSION)"; false; \
	fi


############ Linting and syntax checks ############

.PHONY: lint
lint: ## lint python code
	ruff check setup.py patoolib tests doc/web/source

.PHONY: reformat
reformat: ## format the python code
	ruff format setup.py patoolib tests doc/web/source

.PHONY: checkoutdated checkoutdatedpy checkoutdatedgh
checkoutdated: checkoutdatedpy checkoutdatedgh

checkoutdatedpy:	## Check for outdated package requirements
# Compare the list of currently installed packages with the same list of packages with latest versions from pypi.
# Assumes that all requirements have pinned versions with "==".
# To check only direct dependencies, not those of further down the dependency tree,
# the output is filtered by using `pip tree -d0` and grep with a regular
# expression of the form
# `grep -E "(\tpackage1\t|package2\t| ... |\tpackageN)"`.
# The leading tab before each package prevents matching substrings.
# When grep does not find any match, all required packages are uptodate.
# In this case, grep exits with exitcode 1. Test for this after running grep.
	@set +e; \
	echo "Check for outdated Python packages"; \
	uv pip list --format=freeze |sed 's/==.*//' | uv pip compile - --color=never --quiet --no-deps --no-header --no-annotate |diff <(uv pip list --format=freeze) - --side-by-side --suppress-common-lines | \
	grep -iE "($(shell grep == pyproject.toml  | cut -f1 -d= | tr -d "\"\' "| sed -e 's/\[.*\]//' |sort | paste -sd '|'))"; \
	test $$? = 1

checkoutdatedgh:	## check for outedated github tools
# github-check-outdated is a local tool which compares a given version with the latest available github release version
# see https://gist.github.com/wummel/ef14989766009effa4e262b01096fc8c for an example implementation
	@echo "Check for outdated Github tools"
	github-check-outdated astral-sh uv "$(shell uv self version | cut -f2 -d" ")"


############ Testing ############

.PHONY: test
test: ## run tests
	uv run pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)

# Needs https://nektosact.com/ and docker
# Uses https://github.com/catthehacker/docker_images
.PHONY: test-github
test-github: ## run github workflow actions
	act -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest --matrix os:ubuntu-latest

.PHONY: typecheck
typecheck:	## run pytype
	pytype patoolib

############ Documentation ############

doc/$(APPNAME).txt: doc/$(APPNAME).1 ## make text file from man page for wheel builds
	cols=`stty size | cut -d" " -f2`; stty cols 72; man -l $< | sed -e 's/.\cH//g' > $@; stty cols $$cols

.PHONY: count
count: ## print some code statistics
	@sloccount patoolib

.PHONY: update_webmeta
update_webmeta: ## update package metadata for the homepage
	sed -i -e 's/project =.*/project = "$(APPNAME)"/g' $(WEBMETA)
	sed -i -e 's/version =.*/version = "$(VERSION)"/g' $(WEBMETA)
	sed -i -e 's/author =.*/author = "$(AUTHOR)"/g' $(WEBMETA)

.PHONY: release-homepage
release-homepage: update_webmeta ## update the homepage after a release
	$(MAKE) -C doc/web release
