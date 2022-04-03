# Define ROOTDIR only if not already defined
ROOTDIR?=$(shell realpath .)

WEB_SERVICES:=$(ROOTDIR)/WebService
WEB_SERVICES_SHARED:=$(ROOTDIR)/WebService/SharedCommonCode
REST_API_PORTAL:=$(ROOTDIR)/WebService/RestApiPortal
DATABASE_PORTAL:=$(ROOTDIR)/WebService/DatabaseGateway

DATABASE_TOOLS:=$(ROOTDIR)/InternalTools/DatabaseTools
DEMO_DATABASE_TOOLS:=$(ROOTDIR)/InternalTools/DemoDatabaseTools
UPLOAD_TOOL:=$(ROOTDIR)/InternalTools/UploadPackageAndInitializationVector
CRYPTOGRAPHIC_TOOLS:=$(ROOTDIR)/InternalTools/CryptographicTools

BASE_VM_INIT:=$(ROOTDIR)/VirtualMachine/BaseVmImageInit
VIRTUAL_MACHINE_SHARED:=$(ROOTDIR)/VirtualMachine/SharedComponents

SHARED_COMMON_CODE:=$(ROOTDIR)/SharedCommonCode

ORCHESTRATOR:=$(ROOTDIR)/EndPointTools/Orchestrator
