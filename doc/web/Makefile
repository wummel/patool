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
# Minimal makefile for Sphinx documentation
# You can set these variables from the command line, and also
# from the environment for the first two.
O             ?=
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
# Note: patool-webpage.git is just a checked out copy of patool.git
# where the gh_pages branch is active.
WEBDIR        = $(HOME)/public_html/patool-webpage.git


############ Default target ############
.PHONY: help
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


############ Build and release targets ############

.PHONY: release
release:	sync
	(cd $(WEBDIR); git add .; git commit -m "Updated"; git push)

.PHONY: sync
sync:	html
	cp -r $(BUILDDIR)/html/* $(WEBDIR)/


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
