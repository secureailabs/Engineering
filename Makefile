include Make/Modules.mk
include Make/newwebfrontend.mk

.PHONY: databaseInitializationTool package all clean SharedCommonCode

package_apiservices: SharedCommonCode package_rpcrelated package_smartbroker
	@cp AzureDeploymentTemplates/ArmTemplates/rpcrelated.json ApiServices
	@cp AzureDeploymentTemplates/ArmTemplates/securecomputationnode.json ApiServices
	@cp AzureDeploymentTemplates/ArmTemplates/smartbroker.json ApiServices
	@cp Binary/rpcrelated_dir/package.tar.gz ApiServices
	@cp Binary/smartbroker.tar.gz ApiServices
	@tar --exclude='ApiServices/**venv**' -czvf Binary/apiservices.tar.gz ApiServices
	@rm ApiServices/package.tar.gz
	@rm ApiServices/smartbroker.tar.gz
	@rm ApiServices/rpcrelated.json
	@rm ApiServices/securecomputationnode.json
	@rm ApiServices/smartbroker.json

package_rpcrelated:
	@cd RPCLib && ./package.sh

package_smartbroker:
	@tar --exclude='datascience/**venv**' --exclude='datascience/sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions' --exclude='datascience/**pycache**' --exclude='datascience/.git' --exclude='datascience/.github' -czvf Binary/smartbroker.tar.gz RPCLib/ datascience

package: SharedCommonCode
	@make package_apiservices package_newwebfrontend
	@echo "package done!"

databaseInitializationTool: SharedCommonCode
	@make -C $(DATABASE_INITIALIZATION_TOOL) all
	@echo "databaseInitializationTool done!"

vmInitializer:
	@make -C $(VM_INITIALIZER) all
	@echo "vmInitializer done!"

SharedCommonCode:
	@make -C $(SHARED_COMMON_CODE) all

all: SharedCommonCode
	@make package
	@make databaseInitializationTool vmInitializer
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
