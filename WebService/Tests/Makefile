# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/Make/Common.mk

CXXFLAGS+=
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(shell realpath ../../EndPointTools/RestPortalTester/Sources)
INCLUDE+=-I$(REST_API_PORTAL)/Include

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)

C_SOURCES := $(foreach DIR,$(SRCDIRS),$(C_FINDFILES))
SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
SOURCES+=$(shell realpath ../../EndPointTools/RestPortalTester/Sources/InteractiveClient.cpp)
SOURCES+=$(shell realpath ../../EndPointTools/RestPortalTester/Sources/GuiTerminal.cpp)

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)

OUTPUT=$(ABSROOTDIR)/Binary/$(notdir $(shell pwd))

.PHONY: all, clean, cleanall

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)

clean:
	@rm -rf $(OUTPUT) $(OBJS)

cleanall:
	@rm -rf $(ABSROOTDIR)/Binary
