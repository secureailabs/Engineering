include make/Modules.mk
include make/platformservices.mk
include make/dataservices.mk
include make/webfrontend.mk
include make/securecomputationnode.mk

.PHONY: platformservices dataservices securecomputationnode orchestrator databasetools deployutilities package all clean SharedCommonCode

platformservices: SharedCommonCode
	@make restapiportal platformservices_plugins
	@echo "platformservices done!"

dataservices: SharedCommonCode
	@make databaseportal dataservices_plugins
	@echo "dataservices done!"

orchestrator: SharedCommonCode EndPointTools/Orchestrator
	@make -C EndPointTools/Orchestrator all
	@echo "orchestrator done!"

securecomputationnode: SharedCommonCode
	@make scn_componenets
	@echo "securecomputationnode done!"

package: SharedCommonCode
	@make package_dataservices package_platformservices package_securecomputationnode package_webfrontend
	@echo "package done!"

databasetools:
	@make -C $(DATABASE_TOOLS) all
	@echo "databaseTools done!"

demodatabasetools:
	@make -C $(DEMO_DATABASE_TOOLS) all
	@echo "databaseTools done!"

SharedCommonCode:
	@make -C SharedCommonCode all

all: package databasetools demodatabasetools
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
