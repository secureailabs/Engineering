# The Root directory containing all the code
ROOTDIR=$(shell realpath ../../../..)
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+=
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(REST_API_PORTAL)/Include
INCLUDE+=-I$(WEB_SERVICES_SHARED)/Include

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)
SRCDIRS+=$(REST_API_PORTAL)/Sources
SRCDIRS+=$(WEB_SERVICES_SHARED)/Sources

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
	rm -rf $(OBJS) $(OUTPUT) $(LOCAL_BIN)
