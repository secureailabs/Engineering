DB_PLUGINS = WebService/Plugins/DatabasePortal/DatabaseManager
DB_PLUGINS_SO=$(DB_PLUGINS:WebService/Plugins/DatabasePortal/%=dataservices/SharedLibraries/DatabasePortal/lib%.so)

# These are .PHONY targets but not specified so that the make call to the target is made
# everytime the target is called. If the binary already exists, the build will not happen.
dataservices/SharedLibraries/DatabasePortal/lib%.so: ./WebService/Plugins/DatabasePortal/%
	@echo $<
	@make -C $^ all

databaseportal:
	@make -C $(DATABASE_PORTAL) all

dataservices_plugins: $(DB_PLUGINS_SO)

package_dataservices: $(DB_PLUGINS_SO) databaseportal
	@tar -czvf Binary/DataServices.tar.gz $(DB_PLUGINS_SO) Binary/dataservices/DatabaseGateway
