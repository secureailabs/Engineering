.PHONY: package all clean database_initializer package_rpcrelated package_smartbroker

.SECONDEXPANSION:
package_audit_service: $$(shell find AuditService/ -type f ! -path "AuditService/.*")
	@mkdir -p Binary
	@tar -cvzf Binary/auditserver.tar.gz $^

package_rpcrelated: $$(shell find RPCLib/ -type f ! -path "RPCLib/.*")
	@mkdir -p Binary
	@cp -r datascience Docker/
	@cp datascience/Docker/sail-scn-docker/requirements.txt Docker/datascience/sail-safe-functions
	@tar -cvzf Binary/rpcrelated.tar.gz sail-participant-zeromq $^

package_smartbroker:
	@mkdir -p Binary
	@tar -czvf Binary/smartbroker.tar.gz RPCLib/ sail-aggregator-fastapi

package:
	@make package_audit_service package_rpcrelated
	@echo "package done!"

database_initializer:
	@cd database-initialization && poetry build
	@echo "database_initializer done!"

move_datascience:
	@cp -r datascience Docker/

all:
	@make package
	@make database_initializer
	@echo "All build and packaged!"

clean:
	@rm -rf Docker/datascience
	@rm -rf Binary

clean_datascience:
	@rm -rf Docker/datascience
