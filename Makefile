include make/Modules.mk
include make/platformservices.mk

platformservices: restapiportal plugins
	@echo "platformservices done!"

dataservices:
	@echo "dataservices done!"

backend: dataservices platformservices
	@echo "backend done!"

scn:
	@echo "securecomputationnode done!"

orchestrator:
	@echo "orchestrator done!"

databasetools:
	@echo "databaseTools done!"

deployutilities:
	@echo "deployUtilities done!"

package: backend orchestrator scn
	@echo "package done!"

all: backend
	@echo "All done!"

clean:
	rm -rf Binary
