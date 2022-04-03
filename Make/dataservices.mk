DB_PLUGINS = WebService/Plugins/DatabasePortal/DatabaseManager
DB_PLUGINS_SO=$(DB_PLUGINS:WebService/Plugins/DatabasePortal/%=Binary/dataservices/SharedLibraries/DatabasePortal/lib%.so)

Binary/dataservices/SharedLibraries/DatabasePortal/lib%.so: ./WebService/Plugins/DatabasePortal/%
	@echo $<
	@make -C $^ all

databaseportal:
	@make -C $(DATABASE_PORTAL) all

dataservices_plugins: $(DB_PLUGINS_SO)

package_dataservices: $(DB_PLUGINS_SO) databaseportal
	@tar -czvf Binary/DataServices.tar.gz $(DB_PLUGINS_SO) Binary/dataservices/DatabaseGateway
