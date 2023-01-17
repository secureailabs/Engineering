.PHONY: install
install:
	@poetry install
	@echo "Installing dependencies"
	@cd ../ApiServices/generated/sail-client/ && poetry build
	@poetry run pip3 install ../ApiServices/generated/sail-client/dist/sail_client-0.1.0-py3-none-any.whl

.PHONY: build
build: clean-build
	@echo "Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build:
	@rm -rf dist
