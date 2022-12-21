# Define ROOTDIR only if not already defined
ROOTDIR?=$(shell realpath .)

DATABASE_INITIALIZATION_TOOL:=$(ROOTDIR)/DatabaseInitializationTool
VM_INITIALIZER:=$(ROOTDIR)/VmInitializer
SHARED_COMMON_CODE:=$(ROOTDIR)/SharedCommonCode
