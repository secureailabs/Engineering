# Because of the way make is called, the variables $(BUILD_MODE) and $(ROOTDIR)
# should already be defined
CXXFLAGS=-std=c++17 -fPIC -fstack-protector -DUNIX -DOS_UNIX
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
SRCDIRS :=$(shell realpath ./Sources/)

C_FINDFILES = $(wildcard $(DIR)/*.c)
C_SOURCES := $(foreach DIR,$(SRCDIRS),$(C_FINDFILES))

OBJS=$(C_SOURCES:$(ABSROOTDIR)%.c=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Build/Binaries/libSailCompression.a

.PHONY: all, clean

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.c
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS)
	@mkdir -p $(@D)
	@ar rcs $@ $^

clean:
	@rm -f $(OUTPUT) $(OBJS) 2>/dev/null || :