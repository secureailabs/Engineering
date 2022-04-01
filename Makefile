include make/Modules.mk
include make/platformservices.mk
include make/dataservices.mk
include make/webfrontend.mk
include make/securecomputationnode.mk

.PHONY: platformservices dataservices securecomputationnode orchestrator databaseTools demoDatabaseTools uploadPackageAndInitializationVector package all clean SharedCommonCode

platformservices: SharedCommonCode WebServices_Shared
	@make restapiportal platformservices_plugins
	@echo "platformservices done!"

dataservices: SharedCommonCode
	@make databaseportal dataservices_plugins
	@echo "dataservices done!"

orchestrator: SharedCommonCode EndPointTools/Orchestrator
	@make -C $(ORCHESTRATOR) all
	@echo "orchestrator done!"

securecomputationnode: SharedCommonCode VirtualMachine_Shared
	@make scn_componenets
	@echo "securecomputationnode done!"

package: SharedCommonCode WebServices_Shared VirtualMachine_Shared
	@make package_dataservices package_platformservices package_securecomputationnode package_webfrontend
	@echo "package done!"

databaseTools: SharedCommonCode
	@make -C $(DATABASE_TOOLS) all
	@echo "databaseTools done!"

demoDatabaseTools: SharedCommonCode
	@make -C $(DEMO_DATABASE_TOOLS) all
	@echo "databaseTools done!"

uploadPackageAndInitializationVector: SharedCommonCode
	@make -C $(UPLOAD_TOOL) all
	@echo "databaseTools done!"

baseVmInit: SharedCommonCode
	@make -C $(BASE_VM_INIT) all
	@echo "baseVmInit done!"

SharedCommonCode:
	@make -C $(SHARED_COMMON_CODE) all

WebServices_Shared:
	@make -C $(WEB_SERVICES_SHARED) all

VirtualMachine_Shared:
	@make -C $(VIRTUAL_MACHINE_SHARED) all

all: SharedCommonCode WebServices_Shared VirtualMachine_Shared
	@make package
	@make databaseTools demoDatabaseTools baseVmInit uploadPackageAndInitializationVector
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
