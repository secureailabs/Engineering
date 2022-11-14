# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/Make/Common.mk

OUTPUT_DIR=$(ABSROOTDIR)/Binary/

.PHONY: all, clean

all:
	@mkdir -p $(OUTPUT_DIR)
	@cp vm_initializer.py $(OUTPUT_DIR)
	@cp sample_client.py $(OUTPUT_DIR)
	@cp decrypt_file.py $(OUTPUT_DIR)
