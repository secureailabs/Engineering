ROOTDIR = ..

COMPILER = python3
COMPILERPATH = $(ROOTDIR)/SafeObjectCompiler/main.py

SRCDIR = $(shell realpath ./)
DESDIR = $(shell realpath ../SafeObjects/)

FINDFILES = $(wildcard $(SRCDIR)/*.py)
SOURCES := $(foreach DIR, $(SRCDIR), $(FINDFILES))

OBJS= $(SOURCES:$(SRCDIR)%.py=$(DESDIR)%.safe)

OUTPUT = $(DESDIR)/$(notdir $(shell pwd))

.PHONY: all, cleanall

all: $(OBJS)

$(DESDIR)%.safe: $(SRCDIR)%.py
	@mkdir -p $(@D)
	$(COMPILER) $(COMPILERPATH) $(SRCDIR) $(DESDIR) $(notdir $^)

cleanall:
	rm -rf $(OUTPUT) $(OBJS)
