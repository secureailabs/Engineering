include Make/Modules.mk
include Make/newwebfrontend.mk

.PHONY: package all clean sail_client database_initializer vmInitializer package_apiservices package_rpcrelated package_smartbroker

package_apiservices: SharedCommonCode package_rpcrelated package_smartbroker
	@cp AzureDeploymentTemplates/ArmTemplates/rpcrelated*.json ApiServices
	@cp AzureDeploymentTemplates/ArmTemplates/smartbroker*.json ApiServices
	@cp Binary/rpcrelated_dir/package.tar.gz ApiServices
	@cp Binary/smartbroker.tar.gz ApiServices
	@tar --exclude='ApiServices/**venv**' -czvf Binary/apiservices.tar.gz ApiServices
	@rm ApiServices/package.tar.gz
	@rm ApiServices/smartbroker.tar.gz
	@rm ApiServices/rpcrelated*.json
	@rm ApiServices/smartbroker*.json

package_rpcrelated:
	@cd RPCLib && ./package.sh

package_smartbroker:
	@tar --exclude='datascience/**venv**' --exclude='datascience/sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions' --exclude='datascience/**pycache**' --exclude='datascience/.git' --exclude='datascience/.github' -czvf Binary/smartbroker.tar.gz RPCLib/ datascience

package:
	@make package_apiservices package_newwebfrontend
	@echo "package done!"

sail_client:
	@cd ApiServices/generated/sail-client && poetry build
	@echo "sail_client done!"

database_initializer:
	@cd database-initialization && poetry build
	@echo "database_initializer done!"

vmInitializer:
	@make -C $(VM_INITIALIZER) all
	@echo "vmInitializer done!"

all:
	@make package
	@make sail_client database_initializer
	@make vmInitializer
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
