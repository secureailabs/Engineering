# The Root directory containing all the code
ROOTDIR=$(shell realpath ../..)
include $(ROOTDIR)/Make/Common.mk

CXXFLAGS+= -Wall -g -MMD -MP -fPIC -Werror
LDFLAGS += -Xlinker -export-dynamic -shared -lutil -lm -lpython3.8

# Add the new include folders here
PYTHONINC = /usr/include/python3.8
INCLUDE += -isystem$(PYTHONINC)

INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(shell realpath ../../VirtualMachine/SharedComponents/Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)
SRCDIRS+=$(shell realpath ../../VirtualMachine/SharedComponents/Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)

OUTPUT=$(ABSROOTDIR)/Binary/SAILPyAPI.so

.PHONY: all, clean, cleanall

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)
	@cp $@ ./sail/sail/

cleanall:
	rm -rf $(ABSROOTDIR)/Binary
