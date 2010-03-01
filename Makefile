# This Makefile is only used by developers.
VERSION:=$(shell python setup.py --version)
ARCHIVE:=patool-$(VERSION).tar.gz
PY_FILES_DIRS := patool setup.py patoolib tests
# which test modules to run
TESTS ?= tests/
# set test options, eg. to "--nologcapture"
TESTOPTS=

all:


.PHONY: chmod
chmod:
	-chmod -R a+rX,u+w,go-w -- *
	find . -type d -exec chmod 755 {} \;

.PHONY: dist
dist:
	git archive --format=tar --prefix=patool-$(VERSION)/ HEAD | gzip -9 > ../$(ARCHIVE)
	sha1sum ../$(ARCHIVE) > ../$(ARCHIVE).sha1
#	cd .. && zip -r - patool-git -x "**/.git/**" > $(HOME)/temp/share/patool-devel.zip

# The check programs used here are mostly local scripts on my private system.
# So for other developers there is no need to execute this target.
.PHONY: check
check:
	[ ! -d .svn ] || check-nosvneolstyle -v
	check-copyright
	check-pofiles -v
	py-tabdaddy
	$(MAKE) pyflakes

.PHONY: pyflakes
pyflakes:
	pyflakes $(PY_FILES_DIRS)

.PHONY: count
count:
	@sloccount patool patoolib | grep "Total Physical Source Lines of Code"

.PHONY: clean
clean:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete
	rm -rf build dist

.PHONY: test
test:
	nosetests -v -m "^test_.*" $(TESTOPTS) $(TESTS)

doc/patool.txt: doc/patool.1
	man -l doc/patool.1 | perl -pe 's/.\cH//g' > doc/patool.txt

.PHONY: deb
deb:
	git-buildpackage --git-export-dir=../build-area/ --git-upstream-branch=master --git-debian-branch=debian  --git-ignore-new
