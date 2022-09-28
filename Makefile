include Make/Modules.mk
include Make/webfrontend.mk
include Make/newwebfrontend.mk
include Make/securecomputationnode.mk

.PHONY: securecomputationnode orchestrator datasetViewer databaseInitializationTool safeFunctionCompiler package all clean SharedCommonCode

remoteDataConnector: SharedCommonCode
	@make -C $(REMOTE_DATA_CONNECTOR) all
	@echo "orchestrator done!"

package_apiservices: SharedCommonCode package_rpcrelated
	@cp AzureDeploymentTemplates/ArmTemplates/rpcrelated.json ApiServices
	@cp Binary/rpcrelated_dir/package.tar.gz ApiServices
	@tar --exclude='ApiServices/**venv**' -czvf Binary/apiservices.tar.gz ApiServices
	@rm ApiServices/SecureComputationNode.tar.gz
	@rm ApiServices/rpcrelated.json

package_rpcrelated:
	@cd RPCLib && ./package.sh

orchestrator: SharedCommonCode EndPointTools/Orchestrator
	@make -C $(ORCHESTRATOR) all
	@echo "orchestrator done!"

securecomputationnode: SharedCommonCode VirtualMachine_Shared
	@make scn_componenets
	@echo "securecomputationnode done!"

package: SharedCommonCode VirtualMachine_Shared
	@make package_apiservices package_securecomputationnode package_webfrontend package_newwebfrontend orchestrator
	@echo "package done!"

safeFunctioncompiler: SharedCommonCode
	@make -C $(SAFE_OBJECT_COMPILER) all
	@echo "safefunctioncompiler done!"

datasetViewer: SharedCommonCode
	@make -C $(DATASET_VIEWER_TOOL) all
	@echo "datasetViewer done!"

databaseInitializationTool: SharedCommonCode
	@make -C $(DATABASE_INITIALIZATION_TOOL) all
	@echo "databaseInitializationTool done!"

vmInitializer:
	@make -C $(VM_INITIALIZER) all
	@echo "vmInitializer done!"

SharedCommonCode:
	@make -C $(SHARED_COMMON_CODE) all

VirtualMachine_Shared:
	@make -C $(VIRTUAL_MACHINE_SHARED) all

all: SharedCommonCode VirtualMachine_Shared
	@make package
	@make datasetViewer databaseInitializationTool vmInitializer safeFunctionCompiler remoteDataConnector
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
