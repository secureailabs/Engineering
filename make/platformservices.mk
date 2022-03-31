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

platformservices_plugins: $(PS_PLUGINS_SO)

package_platformservices: $(PS_PLUGINS_SO) restapiportal
	@tar -czvf Binary/PlatformServices.tar.gz $(PS_PLUGINS_SO) Binary/platformservices/RestApiPortal
