.PHONY: install
install:
	@poetry install
	@poetry run install
	@poetry shell

.PHONY: build
build: clean-build
	@echo "Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build:
	@rm -rf dist
