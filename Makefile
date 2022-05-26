include Make/Modules.mk
include Make/platformservices.mk
include Make/dataservices.mk
include Make/webfrontend.mk
include Make/securecomputationnode.mk

.PHONY: platformservices dataservices securecomputationnode orchestrator datasetViewer databaseInitializationTool uploadPackageAndInitializationVector safeFunctionCompiler package all clean SharedCommonCode

package_apiservices: SharedCommonCode uploadPackageAndInitializationVector package_securecomputationnode
	@cp AzureDeploymentTemplates/ArmTemplates/securecomputationnode.json ApiServices
	@cp Binary/UploadPackageAndInitializationVector ApiServices
	@cp Binary/SecureComputationNode.tar.gz ApiServices
	@tar --exclude='ApiServices/dev_env2' -czvf Binary/apiservices.tar.gz ApiServices

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
	@make package_dataservices package_platformservices package_securecomputationnode package_webfrontend orchestrator
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

uploadPackageAndInitializationVector: SharedCommonCode
	@make -C $(UPLOAD_TOOL) all
	@echo "uploadPackageAndInitializationVector done!"

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
	@make datasetViewer databaseInitializationTool baseVmInit uploadPackageAndInitializationVector safeFunctionCompiler
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
