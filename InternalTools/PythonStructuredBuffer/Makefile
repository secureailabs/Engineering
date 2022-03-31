# The Root directory containing all the code
ROOTDIR=../..
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+= -Wall -g -MMD -MP -fPIC
LDFLAGS += -Xlinker -export-dynamic -shared -lm -lpython3.8

# Add the new include folders here
PYTHONINC = /usr/include/python3.8
INCLUDE += -isystem$(PYTHONINC)

INCLUDE+=-I$(shell realpath ./)
INCLUDE+=-I$(shell realpath ../../SharedCommonCode/Include)

# Add the new source directory here
SRCDIRS+=$(shell realpath ./)
SRCDIRS+=$(shell realpath ../../SharedCommonCode/Sources)

FINDFILES = $(wildcard $(DIR)/*.cpp)
SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/PyStructuredBuffer.so

.PHONY: all, clean, cleanall

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS) $(LDLIBS)
	@cp $@ ./

cleanall:
	rm -rf $(ABSROOTDIR)/Binary
