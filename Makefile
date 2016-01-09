# This Makefile is only used by developers.
PYTHON:=python
VERSION:=$(shell $(PYTHON) setup.py --version)
MAINTAINER:=$(shell $(PYTHON) setup.py --maintainer)
AUTHOR:=$(shell $(PYTHON) setup.py --author)
APPNAME:=$(shell $(PYTHON) setup.py --name)
ARCHIVE_SOURCE:=$(APPNAME)-$(VERSION).tar.gz
ARCHIVE_WHEEL:=$(APPNAME)-$(VERSION)-py2.py3-none-any.whl
GITUSER:=wummel
GITREPO:=$(APPNAME)
HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WEBMETA:=doc/web/app.yaml
# Pytest options:
# --resultlog: write test results in file
# -s: do not capture stdout/stderr (some tests fail otherwise)
PYTESTOPTS?=--resultlog=testresults.txt -s
# which test modules to run
TESTS ?= tests/
# set test options
TESTOPTS=

all:


dist:
	[ -d dist ] || mkdir dist
	$(PYTHON) setup.py sdist --formats=tar bdist_wheel
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
	@echo "maintainer: \"$(MAINTAINER)\"" >> $(WEBMETA)
	@echo "author: \"$(AUTHOR)\"" >> $(WEBMETA)
	git add $(WEBMETA)
	git cm "Updated web meta data."

homepage: update_webmeta
# relase website
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
	$(PYTHON) setup.py register

releasecheck: test check
	@if egrep -i "xx\.|xxxx|\.xx" doc/changelog.txt > /dev/null; then \
	  echo "Could not release: edit doc/changelog.txt release date"; false; \
	fi
	@if ! head -n1 doc/changelog.txt | egrep "^$(VERSION)" >/dev/null; then \
	  echo "Could not release: different versions in doc/changelog.txt and setup.py"; \
	  echo "Version in doc/changelog.txt:"; head -n1 doc/changelog.txt; \
	  echo "Version in setup.py: $(VERSION)"; false; \
	fi
	$(PYTHON) setup.py check --restructuredtext

check:
# The check programs used here are mostly local scripts on my private system.
# So for other developers there is no need to execute this target.
	check-copyright setup.py patool patoolib tests
	check-pofiles -v
	py-tabdaddy
	py-unittest2-compat tests/
	$(MAKE) doccheck

doccheck:
	py-check-docstrings --force \
	  patoolib \
	  patool \
	  *.py

pyflakes:
	pyflakes setup.py patool patoolib tests

count:
# print some code statistics
	@sloccount patool patoolib

clean:
	-$(PYTHON) setup.py clean --all
	find . -name '*.py[co]' -exec rm -f {} \;

distclean:	clean
	rm -rf build dist $(APPNAME).egg-info
	rm -f _$(APPNAME)_configdata.py MANIFEST
# clean aborted dist builds and output files
	rm -f testresults.txt
	rm -rf $(APPNAME)-$(VERSION)
	rm -f *-stamp*

localbuild:
	$(PYTHON) setup.py build

test:	localbuild
	$(PYTHON) -m pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)

doc/$(APPNAME).txt: doc/$(APPNAME).1
# make text file from man page for wheel builds
	cols=`stty size | cut -d" " -f2`; stty cols 72; man -l $< | sed -e 's/.\cH//g' > $@; stty cols $$cols

update-copyright:
# update-copyright is a local tool which updates the copyright year for each
# modified file.
	update-copyright --holder="$(MAINTAINER)"

changelog:
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	github-changelog $(DRYRUN) $(GITUSER) $(GITREPO) doc/changelog.txt

.PHONY: changelog update-copyright test clean count pyflakes check
.PHONY: releasecheck release upload sign dist all tag register homepage
.PHONY: localbuild doccheck
