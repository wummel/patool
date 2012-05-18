OXYGEN := ${HOME}/src/oxygen-gitsvn
ICOICONS := logo16x16.png logo32x32.png

all:	favicon.ico

logo%.png:	$(OXYGEN)/%/apps/utilities-file-archiver.png
	cp $< $@

favicon.ico:	$(ICOICONS)
	png2ico favicon.ico $(ICOICONS)
