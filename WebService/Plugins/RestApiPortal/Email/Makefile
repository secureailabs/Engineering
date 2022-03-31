# The Root directory containing all the code
ROOTDIR=../../../..
ABSROOTDIR=$(shell realpath $(ROOTDIR))

OUTPUT=$(ABSROOTDIR)/Binary/platformservices/$(notdir $(shell pwd))/

.PHONY: all, clean

all:
	@mkdir -p $(OUTPUT)
	@cp *.py $(OUTPUT)

clean:
	rm -rf $(OUTPUT)
