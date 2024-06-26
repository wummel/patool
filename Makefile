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
VERSION:=$(shell grep "Version =" patoolib/configuration.py | cut -d '"' -f2)
AUTHOR:=$(shell grep "MyName =" patoolib/configuration.py | cut -d '"' -f2)
APPNAME:=$(shell grep "AppName =" patoolib/configuration.py | cut -d '"' -f2)
ARCHIVE_SOURCE:=$(APPNAME)-$(VERSION).tar.gz
ARCHIVE_WHEEL:=$(APPNAME)-$(VERSION)-py2.py3-none-any.whl
GITUSER:=wummel
GITREPO:=$(APPNAME)
HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WEBMETA:=doc/web/source/conf.py
CHANGELOG:=doc/changelog.txt
GIT_MAIN_BRANCH:=master
PIP_VERSION:=24.1
# Pytest options:
# -s: do not capture stdout/stderr (some tests fail otherwise)
# --full-trace: print full stacktrace on keyboard interrupts
# --log-file: write test output to file for easier inspection
PYTESTOPTS?=-s --full-trace --log-file=build/test.log
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

.PHONY: init ## install pip and required development packages
init:	requirements-dev.txt
	pip install --upgrade pip==$(PIP_VERSION)
	pip install -r $<

.PHONY: localbuild ## install patool in local environment
localbuild:
	pip install --editable .


############ Build and release targets ############

.PHONY: clean
clean: ## remove generated python, web page files and all local patool installations
	python setup.py clean --all
	pip uninstall --yes patool
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
	python setup.py sdist bdist_wheel

.PHONY: upload
upload: ## upload a new release to pypi
	twine upload --config-file $(XDG_CONFIG_HOME)/pypirc \
	  dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_WHEEL)

.PHONY: hub
hub: ## add and push a github release
	hub release create -a dist/$(ARCHIVE_SOURCE) -a dist/$(ARCHIVE_WHEEL) upstream/$(VERSION)

# Make a new release by calling all the distinct steps in the correct order.
# Each step is a separate target so that it's easy to do this manually if
# anything screwed up.
.PHONY: release
release: distclean releasecheck ## release a new version of patool
	$(MAKE) dist hub upload homepage github-issues

.PHONY: releasecheck
releasecheck: checkgit checkchangelog lint test ## check that repo is ready for release

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

.PHONY: github-issues
github-issues: ## close github issues mentioned in changelog
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	cd .. && github-changelog $(DRYRUN) $(GITUSER) $(GITREPO) patool.git/doc/changelog.txt


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

.PHONY: checkoutdated
checkoutdated: ## Check for outdated Python requirements
# Assumes that all requirements have pinned versions with "==".
# Filter the output of `pip list --outdated` using grep with a regular
# expression of the form
# `grep -E "(package1 |package2 | ... |packageN )"`.
# The trailing space after each package prevents matching substrings.
# When grep does not find any match, all packages are uptodate.
# In this case, grep exits with exitcode 1. Test for this after running grep.
	@set +e; \
	echo "Check for outdated Python packages"; \
	pip list --format=columns --outdated | \
	  grep -E "($(shell cat requirements-dev.txt | grep == | cut -f1 -d= | sort | paste -sd '|' | sed -e 's/|/ |/g') )"; \
	test $$? = 1


############ Testing ############

.PHONY: test
test: ## run tests
	pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)


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

.PHONY: homepage
homepage: update_webmeta ## update the homepage after a release
	$(MAKE) -C doc/web release

