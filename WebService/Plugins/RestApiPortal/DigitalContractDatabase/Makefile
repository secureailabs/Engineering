# The Root directory containing all the code
ROOTDIR=../../../..
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+=
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(shell realpath ../../../../WebService/SharedCommonCode/Include)
INCLUDE+=-I$(shell realpath ../../../../WebService/RestApiPortal/Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)
SRCDIRS+=$(shell realpath ../../../../WebService/RestApiPortal/Sources)
SRCDIRS+=$(shell realpath ../../../../WebService/SharedCommonCode/Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/platformservices/SharedLibraries/RestApiPortal/lib$(notdir $(shell pwd)).so

.PHONY: all, clean

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) -shared $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)

clean:
	@rm -rf $(OBJS) $(OUTPUT) $(LOCAL_BIN)
