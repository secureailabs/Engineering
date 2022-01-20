ROOTDIR = ..

COMPILER = python3
DOCMAKER = pdoc
COMPILERPATH = $(ROOTDIR)/SafeObjectCompiler/main.py

SRCDIR = $(shell realpath ./)
DESDIR = $(shell realpath ../SafeObjects/)

FINDFILES = $(wildcard $(SRCDIR)/*.py)
SOURCES := $(foreach DIR, $(SRCDIR), $(FINDFILES))

OBJS= $(SOURCES:$(SRCDIR)%.py=$(DESDIR)%.safe)

DOCS = $(DESDIR)/doc.md

.PHONY: all, cleanall

all: $(OBJS)

$(DESDIR)%.safe: $(SRCDIR)%.py
	@mkdir -p $(@D)
	$(COMPILER) $(COMPILERPATH) $(SRCDIR) $(DESDIR) $(notdir $^)

doc:
	$(DOCMAKER) --pdf *.py > $(DOCS)

cleanall:
	rm -rf $(OUTPUT) $(OBJS)
