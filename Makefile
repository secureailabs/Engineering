include Make/Modules.mk
include Make/newwebfrontend.mk

.PHONY: package all clean sail_client database_initializer package_apiservices package_rpcrelated package_smartbroker

package_apiservices: package_rpcrelated package_smartbroker
	@mkdir -p Binary
	@cp AzureDeploymentTemplates/ArmTemplates/sailvm*.json ApiServices
	@cp Binary/rpcrelated.tar.gz ApiServices
	@cp Binary/smartbroker.tar.gz ApiServices
	@tar --exclude='ApiServices/**venv**' -czvf Binary/apiservices.tar.gz ApiServices
	@rm ApiServices/smartbroker.tar.gz
	@rm ApiServices/rpcrelated.tar.gz
	@rm ApiServices/sailvm*.json

.SECONDEXPANSION:
package_audit_service: $$(shell find AuditService/ -type f ! -path "AuditService/.*")
	@mkdir -p Binary
	@tar -cvzf Binary/auditserver.tar.gz $^

package_rpcrelated: $$(shell find RPCLib/ -type f ! -path "RPCLib/.*")
	@mkdir -p Binary
	@cp -r datascience Docker/rpcrelated
	@chmod -R 777 Docker/rpcrelated/datascience
	@cp datascience/Docker/sail-scn-docker/requirements.txt Docker/rpcrelated/datascience/sail-safe-functions
	@tar --exclude='datascience/.*' --exclude='datascience/notebooks' --exclude='datascience/**venv**' --exclude='datascience/sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions' --exclude='datascience/**pycache**' -cvzf Binary/rpcrelated.tar.gz datascience $^

package_smartbroker:
	@mkdir -p Binary
	@tar --exclude='datascience/**venv**' --exclude='datascience/sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions' --exclude='datascience/**pycache**' --exclude='datascience/.git' --exclude='datascience/.github' -czvf Binary/smartbroker.tar.gz RPCLib/ datascience

package:
	@make package_audit_service package_apiservices package_newwebfrontend package_rpcrelated
	@echo "package done!"

sail_client:
	@cd ApiServices/generated/sail-client && poetry build
	@echo "sail_client done!"

database_initializer:
	@cd database-initialization && poetry build
	@echo "database_initializer done!"

all:
	@make package
	@make sail_client database_initializer
	@echo "All build and packaged!"

clean:
	@rm -rf Docker/rpcrelated/datascience
	@rm -rf Binary

clean_datascience:
	@rm -rf Docker/rpcrelated/datascience
