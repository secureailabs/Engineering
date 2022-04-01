# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+=-rdynamic
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/dataservices/$(notdir $(shell pwd))

.PHONY: all, clean, cleanall

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
