# The Root directory containing all the code
ROOTDIR=$(shell realpath ../../../..)
include $(ROOTDIR)/make/Common.mk

CXXFLAGS+=
LDFLAGS+= -lmongocxx -lbsoncxx -lcurl

# Add the new include folders here
INCLUDE+=-I$(shell realpath ./Include)
INCLUDE+=-I$(shell realpath ../../../../WebService/DatabaseGateway/Include)
INCLUDE+=-I$(CRYPTOGRAPHIC_TOOLS)/Include
INCLUDE+=-I$(shell realpath ../../../../WebService/Plugins/RestApiPortal/CryptographicKeyManagement)
# Includes for MongoDB C++ driver
INCLUDE+=-I/usr/local/include/mongocxx/v_noabi -I/usr/local/include/libmongoc-1.0 -I/usr/local/include/bsoncxx/v_noabi -I/usr/local/include/libbson-1.0 -L/usr/local/lib

# Add the new source directory here
SRCDIRS+=$(shell realpath ./Sources)
SRCDIRS+=$(shell realpath ../../../../WebService/DatabaseGateway/Sources)

SOURCES := $(foreach DIR,$(SRCDIRS),$(FINDFILES))
SOURCES += $(shell realpath ../../../../InternalTools/CryptographicTools/Sources/CryptoUtils.cpp)
SOURCES += $(shell realpath ../../../../WebService/Plugins/RestApiPortal/CryptographicKeyManagement/CryptographicEngine.cpp)
SOURCES += $(shell realpath ../../../../WebService/Plugins/RestApiPortal/CryptographicKeyManagement/CryptographicKey.cpp)
SOURCES += $(shell realpath ../../../../WebService/Plugins/RestApiPortal/CryptographicKeyManagement/CryptographyHelperFunctions.cpp)

OBJS=$(SOURCES:$(ABSROOTDIR)%.cpp=$(OBJDIR)%.o)
OUTPUT=$(ABSROOTDIR)/Binary/dataservices/SharedLibraries/DatabasePortal/lib$(notdir $(shell pwd)).so

.PHONY: all,clean

all: $(OUTPUT)

$(OBJDIR)%.o: $(ABSROOTDIR)%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $^ -o $@

$(OUTPUT): $(OBJS) SharedCommonCode
	@mkdir -p $(@D)
	$(CXX) -shared $(CXXFLAGS) $(INCLUDE) $(filter %.o,$^) -o $@ $(LDFLAGS)

clean:
	rm -rf $(OBJS) $(OUTPUT) $(LOCAL_BIN)
