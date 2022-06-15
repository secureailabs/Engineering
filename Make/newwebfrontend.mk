package_newwebfrontend:
	@rm -rf NewWebFrontend/client/node_modules
	@rm -rf NewWebFrontend/server/node_modules
	@tar -czvf Binary/newwebfrontend.tar.gz NewWebFrontend
