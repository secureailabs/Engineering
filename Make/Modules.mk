# Define ROOTDIR only if not already defined
ROOTDIR?=$(shell realpath .)

DATASET_VIEWER_TOOL:=$(ROOTDIR)/InternalTools/DatasetViewer
DATABASE_INITIALIZATION_TOOL:=$(ROOTDIR)/InternalTools/DatabaseInitializationTool
SAFE_OBJECT_COMPILER:=$(ROOTDIR)/EndPointTools/SafeObjectTools/SafeObjectCompiler/Source
CRYPTOGRAPHIC_TOOLS:=$(ROOTDIR)/InternalTools/CryptographicTools
REMOTE_DATA_CONNECTOR:=$(ROOTDIR)/InternalTools/RemoteDataConnector

VM_INITIALIZER:=$(ROOTDIR)/VmInitializer
VIRTUAL_MACHINE_SHARED:=$(ROOTDIR)/VirtualMachine/SharedComponents

SHARED_COMMON_CODE:=$(ROOTDIR)/SharedCommonCode

ORCHESTRATOR:=$(ROOTDIR)/EndPointTools/Orchestrator
