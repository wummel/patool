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
PIP_VERSION:=23.3.1
# Pytest options:
# -s: do not capture stdout/stderr (some tests fail otherwise)
# --full-trace: print full stacktrace on keyboard interrupts
PYTESTOPTS?=-s --full-trace
# which test modules to run
TESTS ?= tests/
# set test options
TESTOPTS=

############ Default target ############

.PHONY: help
help:	## display this help section
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help


############ Installation and provisioning  ############

.PHONY: init
init:	requirements-dev.txt
	pip install --upgrade pip==$(PIP_VERSION)
	pip install -r $<

.PHONY: localbuild
localbuild:
	pip install --editable .


############ Build and release targets ############

.PHONY: clean
clean:
	python setup.py clean --all
	pip uninstall --yes patool
	$(MAKE) -C doc/web clean

.PHONY: distclean
distclean:	clean
	rm -rf build dist $(APPNAME).egg-info
	rm -f MANIFEST
# clean aborted dist builds and output files
	rm -f testresults.txt
	rm -rf $(APPNAME)-$(VERSION)
	rm -f *-stamp*

.PHONY: dist
dist:
	python setup.py sdist bdist_wheel

.PHONY: upload
upload:
	twine upload --config-file $(XDG_CONFIG_HOME)/pypirc \
	  dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_WHEEL)

.PHONY: tag
tag:
# add and push the version tag
	git tag upstream/$(VERSION)
	git push --tags origin upstream/$(VERSION)

# Make a new release by calling all the distinct steps in the correct order.
# Each step is a separate target so that it's easy to do this manually if
# anything screwed up.
.PHONY: release
release: distclean releasecheck
	$(MAKE) dist upload homepage tag github-issues

.PHONY: releasecheck
releasecheck: checkgit checkchangelog lint test

checkgit:
# check that branch is master
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then \
	  echo "ERROR: current branch is not 'master'"; \
	  git rev-parse --abbrev-ref HEAD; \
	  false; \
	fi
# check for uncommitted versions
	@if [ -n "$(shell git status --porcelain --untracked-files=all)" ]; then \
	  echo "ERROR: uncommitted changes"; \
	  git status --porcelain --untracked-files=all; \
	  false; \
	fi

github-issues:
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	cd .. && github-changelog $(DRYRUN) $(GITUSER) $(GITREPO) patool.git/doc/changelog.txt


############ Versioning ############

# shortcut target for bumpversion: bumpversion-{major,minor,patch}
bumpversion-%:
	bumpversion $*
	$(MAKE) bumpchangelog

bumpchangelog:
	sed -i '1i$(VERSION) (released xx.xx.xxxx)\n  *\n' $(CHANGELOG)

# check changelog before release
checkchangelog:
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
lint:
	ruff setup.py patoolib tests doc/web/source

.PHONY: reformat
reformat:
	ruff --fix setup.py patoolib tests doc/web/source

.PHONY: checkoutdated
checkoutdated:
	pip list --format=columns --outdated


############ Testing ############

.PHONY: test
test:
	pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)


############ Documentation ############

doc/$(APPNAME).txt: doc/$(APPNAME).1
# make text file from man page for wheel builds
	cols=`stty size | cut -d" " -f2`; stty cols 72; man -l $< | sed -e 's/.\cH//g' > $@; stty cols $$cols

.PHONY: count
count:
# print some code statistics
	@sloccount patoolib

.PHONY: update_webmeta
update_webmeta:
# update metadata
	sed -i -e 's/project =.*/project = "$(APPNAME)"/g' $(WEBMETA)
	sed -i -e 's/version =.*/version = "$(VERSION)"/g' $(WEBMETA)
	sed -i -e 's/author =.*/author = "$(AUTHOR)"/g' $(WEBMETA)

.PHONY: homepage
homepage: update_webmeta
# release website
	$(MAKE) -C doc/web release
