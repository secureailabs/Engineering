.PHONY: all clean database_initializer

database_initializer:
	@cd database-initialization && poetry build
	@echo "database_initializer done!"

all:
	@make database_initializer
	@echo "All build and packaged!"

clean:
	@rm -rf Binary
