HOMEPAGE:=$(HOME)/public_html/patool-webpage.git
WOK:=$(HOME)/projects/wok.git/wok

all:

media/favicon.ico:	../icon/favicon.ico
	cp $< $@

gen:	media/favicon.ico
	$(WOK) -v

serve:	gen
	xdg-open http://localhost:8080
	$(WOK) --server localhost:8080

upload:
	cd $(HOMEPAGE) && git add . && git commit -m "Updated" && git push

release: gen upload

.PHONY: all gen serve upload release
