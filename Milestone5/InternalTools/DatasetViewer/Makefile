# Because of the way make is called, the variables $(BUILD_MODE) and $(ROOTDIR)
# should already be defined
CXXFLAGS=-std=c++17 -fPIC -fstack-protector -DUNIX -DOS_UNIX
LDFLAGS=-lSharedCommonCode -lSailCompression -lpthread -ldl -luuid -lrt -lcrypto -lssl -lcurl
# The $(BUILD_MODE) value is set as a command line parameter into make by BuiltTool
BUILD_MODE?=$(MODE)
ifeq ($(BUILD_MODE), debug)
	CXXFLAGS+= -ggdb
else
	CXXFLAGS+= -O3
endif

ABSROOTDIR=$(ROOT)
OBJDIR=$(ABSROOTDIR)/Build/Binaries/Objects

INCLUDE :=-I$(shell realpath ./Include/)
INCLUDE +=-I$(shell realpath $(ABSROOTDIR)/Build/Include)
SRCDIRS :=$(shell realpath ./Sources/)
LDFLAGS +=-L$(shell realpath $(ABSROOTDIR)/Build/Libraries)

CPP_FINDFILES=$(wildcard $(DIR)/*.cpp)
CPP_SOURCES := $(foreach DIR,$(SRCDIRS),$(CPP_FINDFILES))

OBJS=$(CPP_SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Build/Binaries/$(notdir $(shell pwd))

.PHONY: all, clean

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)

clean:
	@rm $(OUTPUT) $(OBJS) 2>/dev/null || :
