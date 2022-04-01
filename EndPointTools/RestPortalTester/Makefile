CXXFLAGS=-std=c++17 -fPIC -fstack-protector -DUNIX -DOS_UNIX -fPIC
LDFLAGS=-lSharedCommonCode -lpthread -ldl -luuid -lrt -lcrypto -lssl -lstdc++fs -lssl -lcurl

# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
ABSROOTDIR=$(shell realpath $(ROOTDIR))
OBJDIR=$(ABSROOTDIR)/Binary/Objects

# Build rules for the SharedCommonCode directory
include $(ROOTDIR)/make/Common.mk

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(SHARED_COMMON_CODE)/Include
INCLUDE+=-I$(shell realpath ../../WebService/RestApiPortal/Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)

FINDFILES = $(wildcard $(DIR)/*.cpp)
SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/$(notdir $(shell pwd))

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS) $(LDLIBS)

clean:
	rm -rf $(OUTPUT) $(OBJS)

cleanall:
	rm -rf $(ABSROOTDIR)/Binary
