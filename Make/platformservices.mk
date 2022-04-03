PS_PLUGINS = \
WebService/Plugins/RestApiPortal/SailAuthentication \
WebService/Plugins/RestApiPortal/AzureManager \
WebService/Plugins/RestApiPortal/DatasetFamilyManager \
WebService/Plugins/RestApiPortal/VirtualMachineManager \
WebService/Plugins/RestApiPortal/CryptographicKeyManagement \
WebService/Plugins/RestApiPortal/AuditLogManager \
WebService/Plugins/RestApiPortal/RemoteDataConnectorManager \
WebService/Plugins/RestApiPortal/DatasetDatabase \
WebService/Plugins/RestApiPortal/AccountDatabase \
WebService/Plugins/RestApiPortal/DigitalContractDatabase \
WebService/Plugins/RestApiPortal/DataFederationManager

PS_PLUGINS_SO=$(PS_PLUGINS:WebService/Plugins/RestApiPortal/%=Binary/platformservices/SharedLibraries/RestApiPortal/lib%.so)

Binary/platformservices/SharedLibraries/RestApiPortal/lib%.so: ./WebService/Plugins/RestApiPortal/%
	@echo $<
	@make -C $^ all

restapiportal:
	@make -C $(REST_API_PORTAL) all

# TODO: Prawal the web plugins are supposed to be independent and should not depend on other plugins for compilation
# but that is not the case right now. this will be fixed as part of BOARD-1540
# The .NOTPARALLEL build will be removed when we plugins are completely independent of each other.
.NOTPARALLEL: platformservices_plugins package_platformservices
platformservices_plugins: $(PS_PLUGINS_SO)

package_platformservices: $(PS_PLUGINS_SO) restapiportal
	@tar -czvf Binary/PlatformServices.tar.gz $(PS_PLUGINS_SO) Binary/platformservices/RestApiPortal
