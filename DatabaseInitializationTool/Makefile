# The Root directory containing all the code
ROOTDIR=$(shell realpath ..)
include $(ROOTDIR)/Make/Common.mk

CXXFLAGS+=
LDFLAGS+=

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Sources)
SRCDIRS+=$(shell realpath ./Sources)
SAMPLEFILES := $(shell realpath ./SampleFiles)
SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
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
	@cp -f $(SAMPLEFILES)/DatabaseInitializationSettings.json $(ABSROOTDIR)/Binary
	@chmod a+rwx,g+rwx,o+rwx $(ABSROOTDIR)/Binary

clean:
	@rm -rf $(OUTPUT) $(OBJS)

cleanall:
	@rm -rf $(ABSROOTDIR)/Binary
