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

VERSION:=$(shell python setup.py --version)
AUTHOR:=$(shell python setup.py --author)
APPNAME:=$(shell python setup.py --name)
ARCHIVE_SOURCE:=$(APPNAME)-$(VERSION).tar.gz
ARCHIVE_WHEEL:=$(APPNAME)-$(VERSION)-py2.py3-none-any.whl
GITUSER:=wummel
GITREPO:=$(APPNAME)
HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WEBMETA:=doc/web/source/conf.py
PIP_VERSION:=23.3.1
# Pytest options:
# --report-log: write test results in file
# -s: do not capture stdout/stderr (some tests fail otherwise)
PYTESTOPTS?=--report-log=testresults.txt -s
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
	[ -d dist ] || mkdir dist
	python setup.py sdist --formats=tar bdist_wheel
	gzip --best dist/$(APPNAME)-$(VERSION).tar

.PHONY: sign
sign:
	[ -f dist/$(ARCHIVE_SOURCE).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_SOURCE)
	[ -f dist/$(ARCHIVE_WHEEL).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_WHEEL)

.PHONY: upload
upload:
	twine upload dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_SOURCE).asc \
	             dist/$(ARCHIVE_WHEEL) dist/$(ARCHIVE_WHEEL).asc

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
	$(MAKE) dist sign upload homepage tag register changelog

.PHONY: register
register:
	@echo "Register at Python Package Index..."
	python setup.py register

.PHONY: releasecheck
releasecheck: checkgit lint test
	@if egrep -i "xx\.|xxxx|\.xx" doc/changelog.txt > /dev/null; then \
	  echo "Could not release: edit doc/changelog.txt release date"; false; \
	fi
	@if ! head -n1 doc/changelog.txt | egrep "^$(VERSION)" >/dev/null; then \
	  echo "Could not release: different versions in doc/changelog.txt and setup.py"; \
	  echo "Version in doc/changelog.txt:"; head -n1 doc/changelog.txt; \
	  echo "Version in setup.py: $(VERSION)"; false; \
	fi

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

changelog:
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	github-changelog $(DRYRUN) $(GITUSER) $(GITREPO) doc/changelog.txt


############ Linting and syntax checks ############

.PHONY: lint
lint:
	ruff setup.py patoolib tests

.PHONY: reformat
reformat:
	ruff --fix setup.py patoolib tests


############ Testing ############

.PHONY: test
test:
	python -m pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)


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

