MAIN = main
.PHONY: all clean distclean
all: $(MAIN).pdf
$(MAIN).pdf: $(MAIN).tex mysetup.tex references.bib chapters/*.tex latexmkrc
	latexmk $(MAIN).tex
clean:
	latexmk -c $(MAIN).tex
	rm -f chapters/*.aux
distclean: clean
	rm -f $(MAIN).pdf
