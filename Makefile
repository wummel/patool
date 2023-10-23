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
WEBMETA:=doc/web/app.yaml
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

init:	requirements-dev.txt
	pip install --upgrade pip==$(PIP_VERSION)
	pip install -r $<

localbuild:
	pip install --editable .


############ Build and release targets ############

clean:
	python setup.py clean --all
	pip uninstall --yes patool

distclean:	clean
	rm -rf build dist $(APPNAME).egg-info
	rm -f MANIFEST
# clean aborted dist builds and output files
	rm -f testresults.txt
	rm -rf $(APPNAME)-$(VERSION)
	rm -f *-stamp*

dist:
	[ -d dist ] || mkdir dist
	python setup.py sdist --formats=tar bdist_wheel
	gzip --best dist/$(APPNAME)-$(VERSION).tar

sign:
	[ -f dist/$(ARCHIVE_SOURCE).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_SOURCE)
	[ -f dist/$(ARCHIVE_WHEEL).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_WHEEL)

upload:
	twine upload dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_SOURCE).asc \
	             dist/$(ARCHIVE_WHEEL) dist/$(ARCHIVE_WHEEL).asc

update_webmeta:
# update metadata
	@echo "version: \"$(VERSION)\"" > $(WEBMETA)
	@echo "name: \"$(APPNAME)\"" >> $(WEBMETA)
	@echo "author: \"$(AUTHOR)\"" >> $(WEBMETA)
	git add $(WEBMETA)
	git cm "Updated web meta data."

homepage: update_webmeta
# release website
	$(MAKE) -C doc/web release

tag:
# add and push the version tag
	git tag upstream/$(VERSION)
	git push --tags origin upstream/$(VERSION)

# Make a new release by calling all the distinct steps in the correct order.
# Each step is a separate target so that it's easy to do this manually if
# anything screwed up.
release: distclean releasecheck
	$(MAKE) dist sign upload homepage tag register changelog

register:
	@echo "Register at Python Package Index..."
	python setup.py register

releasecheck: test
	@if egrep -i "xx\.|xxxx|\.xx" doc/changelog.txt > /dev/null; then \
	  echo "Could not release: edit doc/changelog.txt release date"; false; \
	fi
	@if ! head -n1 doc/changelog.txt | egrep "^$(VERSION)" >/dev/null; then \
	  echo "Could not release: different versions in doc/changelog.txt and setup.py"; \
	  echo "Version in doc/changelog.txt:"; head -n1 doc/changelog.txt; \
	  echo "Version in setup.py: $(VERSION)"; false; \
	fi
	python setup.py check --restructuredtext


############ Linting and syntax checks ############

lint-py:
	ruff setup.py patoolib tests

reformat:
	ruff --fix setup.py patoolib tests


############ Testing ############

test:
	python -m pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)


############ Documentation ############

doc/$(APPNAME).txt: doc/$(APPNAME).1
# make text file from man page for wheel builds
	cols=`stty size | cut -d" " -f2`; stty cols 72; man -l $< | sed -e 's/.\cH//g' > $@; stty cols $$cols

count:
# print some code statistics
	@sloccount patoolib
