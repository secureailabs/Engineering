# Define ROOTDIR only if not already defined
ROOTDIR?=$(shell realpath .)

WEB_SERVICES:=$(ROOTDIR)/WebService
WEB_SERVICES_SHARED:=$(ROOTDIR)/WebService/SharedCommonCode
REST_API_PORTAL:=$(ROOTDIR)/WebService/RestApiPortal
DATABASE_PORTAL:=$(ROOTDIR)/WebService/DatabaseGateway

DATASET_VIEWER_TOOL:=$(ROOTDIR)/InternalTools/DatasetViewer
DATABASE_INITIALIZATION_TOOL:=$(ROOTDIR)/InternalTools/DatabaseInitializationTool
SAFE_OBJECT_COMPILER:=$(ROOTDIR)/EndPointTools/SafeObjectTools/SafeObjectCompiler/Source
UPLOAD_TOOL:=$(ROOTDIR)/InternalTools/UploadPackageAndInitializationVector
CRYPTOGRAPHIC_TOOLS:=$(ROOTDIR)/InternalTools/CryptographicTools
REMOTE_DATA_CONNECTOR:=$(ROOTDIR)/InternalTools/RemoteDataConnector

BASE_VM_INIT:=$(ROOTDIR)/VirtualMachine/BaseVmImageInit
VIRTUAL_MACHINE_SHARED:=$(ROOTDIR)/VirtualMachine/SharedComponents

SHARED_COMMON_CODE:=$(ROOTDIR)/SharedCommonCode

ORCHESTRATOR:=$(ROOTDIR)/EndPointTools/Orchestrator
