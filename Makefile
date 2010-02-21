PY_FILES_DIRS := patool setup.py patoolib tests
# This Makefile is only used by developers.
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
	git archive --format=zip --prefix=patool-devel/ HEAD > $(HOME)/temp/share/patool-devel.zip
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
	rm -rf build

.PHONY: test
test:
	nosetests -v -m "^test_.*" $(TESTOPTS) $(TESTS)

doc/patool.txt: doc/patool.1
	man -l doc/patool.1 | perl -pe 's/.\cH//g' > doc/patool.txt

.PHONY: deb
deb:
	git-buildpackage --git-export-dir=../build-area/ --git-upstream-branch=master --git-debian-branch=debian  --git-ignore-new
