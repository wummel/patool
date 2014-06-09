# This Makefile is only used by developers.
PYTHON:=python
VERSION:=$(shell $(PYTHON) setup.py --version)
MAINTAINER:=$(shell $(PYTHON) setup.py --maintainer)
AUTHOR:=$(shell $(PYTHON) setup.py --author)
APPNAME:=$(shell $(PYTHON) setup.py --name)
ARCHIVE_SOURCE:=$(APPNAME)-$(VERSION).tar.gz
ARCHIVE_WIN32:=$(APPNAME)-$(VERSION).exe
GITUSER:=wummel
GITREPO:=$(APPNAME)
HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WEBMETA:=doc/web/app.yaml
DEBUILDDIR:=$(HOME)/projects/debian/official
DEBORIGFILE:=$(DEBUILDDIR)/$(APPNAME)_$(VERSION).orig.tar.gz
DEBPACKAGEDIR:=$(DEBUILDDIR)/$(APPNAME)-$(VERSION)
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
	$(PYTHON) setup.py sdist --formats=tar
	gzip --best dist/$(APPNAME)-$(VERSION).tar
	[ ! -f ../$(ARCHIVE_WIN32) ] || cp ../$(ARCHIVE_WIN32) dist

sign:
	[ -f dist/$(ARCHIVE_SOURCE).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_SOURCE)
	[ -f dist/$(ARCHIVE_WIN32).asc ] || gpg --detach-sign --armor dist/$(ARCHIVE_WIN32)

upload:	upload_source upload_binary

upload_source:
	twine upload dist/$(ARCHIVE_SOURCE) dist/$(ARCHIVE_SOURCE).asc

upload_binary:
	cp dist/$(ARCHIVE_WIN32) dist/$(ARCHIVE_WIN32).asc \
	  $(HOMEPAGE)/dist

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
release: clean releasecheck
	$(MAKE) dist sign upload homepage tag register changelog deb

register:
	@echo "Register at Python Package Index..."
	$(PYTHON) setup.py register
	@echo "Submitting to freecode.org..."
	freecode-submit < $(APPNAME).freecode

releasecheck: test check
	@if egrep -i "xx\.|xxxx|\.xx" doc/changelog.txt > /dev/null; then \
	  echo "Could not release: edit doc/changelog.txt release date"; false; \
	fi
	@if [ ! -f ../$(ARCHIVE_WIN32) ]; then \
	  echo "Missing WIN32 distribution archive at ../$(ARCHIVE_WIN32)"; \
	  false; \
	fi
	@if ! grep "Version: $(VERSION)" $(APPNAME).freecode > /dev/null; then \
	  echo "Could not release: edit $(APPNAME).freecode version"; false; \
	fi
	$(PYTHON) setup.py check --restructuredtext

check:
# The check programs used here are mostly local scripts on my private system.
# So for other developers there is no need to execute this target.
	check-copyright
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
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete
	rm -rf build dist

localbuild:
	$(PYTHON) setup.py build

test:	localbuild
	$(PYTHON) -m pytest $(PYTESTOPTS) $(TESTOPTS) $(TESTS)

doc/$(APPNAME).txt: doc/$(APPNAME).1
# make text file from man page for Windows builds
	cols=`stty size | cut -d" " -f2`; stty cols 72; man -l $< | sed -e 's/.\cH//g' > $@; stty cols $$cols

deb:
# build a debian package
	[ -f $(DEBORIGFILE) ] || cp dist/$(ARCHIVE_SOURCE) $(DEBORIGFILE)
	sed -i -e 's/VERSION_$(APPNAME):=.*/VERSION_$(LAPPNAME):=$(VERSION)/' $(DEBUILDDIR)/$(LAPPNAME).mak
	[ -d $(DEBPACKAGEDIR) ] || (cd $(DEBUILDDIR); \
	  patool extract $(DEBORIGFILE); \
	  cd $(CURDIR); \
	  git checkout debian; \
	  cp -r debian $(DEBPACKAGEDIR); \
	  rm -f $(DEBPACKAGEDIR)/debian/.gitignore; \
	  git checkout master)
	$(MAKE) -C $(DEBUILDDIR) $(APPNAME)_clean $(APPNAME)

update-copyright:
# update-copyright is a local tool which updates the copyright year for each
# modified file.
	update-copyright --holder="$(MAINTAINER)"

changelog:
# github-changelog is a local tool which parses the changelog and automatically
# closes issues mentioned in the changelog entries.
	github-changelog $(DRYRUN) $(GITUSER) $(GITREPO) doc/changelog.txt

.PHONY: changelog update-copyright deb test clean count pyflakes check
.PHONY: releasecheck release upload sign dist all tag register homepage
.PHONY: localbuild doccheck
