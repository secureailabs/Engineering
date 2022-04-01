# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+=-std=c++17 -fPIC -fstack-protector -DUNIX -DOS_UNIX
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(WEB_SERVICES_SHARED)/Include

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
C_SOURCES := $(foreach DIR,$(SRCDIRS),$(C_FINDFILES))

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/platformservices/$(notdir $(shell pwd))

.PHONY: all, clean, cleanall

# All our build rules
all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)

clean:
	rm -rf $(OUTPUT) $(OBJS)

cleanall:
	rm -rf $(ABSROOTDIR)/Binary
