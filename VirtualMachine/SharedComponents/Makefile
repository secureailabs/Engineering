# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/Make/Common.mk

CXXFLAGS+=
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)

.PHONY: all, clean

# Just building the object files as that's what we need
all: $(OBJS)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

clean:
	rm -rf $(OBJS)
