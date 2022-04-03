package_webfrontend:
	@rm -rf WebFrontend/client/node_modules
	@rm -rf WebFrontend/server/node_modules
	@tar -czvf Binary/webfrontend.tar.gz WebFrontend
