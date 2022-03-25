DIRECTORY = $(sort $(dir $(wildcard WebService/Plugins/RestApiPortal/*/)))
PLUGINS=$(DIRECTORY:WebService/Plugins/RestApiPortal/%/=%)
PLUGINS_SO=$(DIRECTORY:WebService/Plugins/RestApiPortal/%/=lib%.so)

restapiportal: SharedCommonCode
	@cd $(REST_API_PORTAL) && make all -j

lib%.so: ./WebService/Plugins/RestApiPortal/%
	@echo $<
	# @cd $^ && make all -j

plugins: SharedCommonCode
	@make $(PLUGINS_SO)
