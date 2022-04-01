ifndef ROOTDIR
$(error ROOTDIR is not set. Common.mk can only be included in a file which has ROOTDIR defined)
endif
include $(ROOTDIR)/make/Modules.mk

BUILD_MODE?=debug
CXXFLAGS+=-std=c++17 -fPIC -fstack-protector -DUNIX -DOS_UNIX
LDFLAGS+=-lSharedCommonCode -lpthread -ldl -luuid -lrt -lcrypto -lssl -lstdc++fs -lssl -lcurl

ifeq ($(BUILD_MODE), debug)
	CXXFLAGS+= -ggdb
else
	CXXFLAGS+= -O3
endif

ABSROOTDIR=$(shell realpath $(ROOTDIR))
OBJDIR=$(ABSROOTDIR)/Binary/Objects

FINDFILES = $(wildcard $(DIR)/*.cpp)

# Add common include paths once
INCLUDE+=-I$(SHARED_COMMON_CODE)/Include
INCLUDE+=-I$(shell realpath $(ABSROOTDIR)/ThirdPartyLibraries/LzmaSdk/Include)

# We want to find our own static libraries
LDFLAGS += -L$(ABSROOTDIR)/Binary/StaticLibraries

.PHONY: SharedCommonCode

SharedCommonCode:
	@make -C $(ABSROOTDIR)/SharedCommonCode all
