include Make/Modules.mk
include Make/platformservices.mk
include Make/dataservices.mk
include Make/webfrontend.mk
include Make/securecomputationnode.mk

.PHONY: platformservices dataservices databaseInitializationTool datasetViewer securecomputationnode orchestrator safefunctioncompiler uploadPackageAndInitializationVector package all clean SharedCommonCode

platformservices: SharedCommonCode WebServices_Shared
	@make restapiportal platformservices_plugins
	@echo "platformservices done!"

dataservices: SharedCommonCode
	@make databaseportal dataservices_plugins
	@echo "dataservices done!"

orchestrator: SharedCommonCode EndPointTools/Orchestrator
	@make -C $(ORCHESTRATOR) all
	@echo "orchestrator done!"

safefunctioncompiler: SharedCommonCode
	@make -C $(SAFE_OBJECT_COMPILER) all
	@echo "safefunctioncompiler done!"

securecomputationnode: SharedCommonCode VirtualMachine_Shared
	@make scn_componenets
	@echo "securecomputationnode done!"

package: SharedCommonCode WebServices_Shared VirtualMachine_Shared
	@make package_dataservices package_platformservices package_securecomputationnode package_webfrontend orchestrator
	@echo "package done!"

datasetViewer: SharedCommonCode
	@make -C $(DATASET_VIEWER_TOOL) all
	@echo "datasetViewer done!"
    
databaseInitializationTool: SharedCommonCode
	@make -C $(DATABASE_INITIALIZATION_TOOL) all
	@echo "databaseInitializationTool done!"
    
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
	@make databaseInitializationTool datasetViewer baseVmInit uploadPackageAndInitializationVector safefunctioncompiler
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
