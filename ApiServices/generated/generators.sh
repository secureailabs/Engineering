# delete existing openapi.json
rm -f docs/openapi.json

# Download the API spec
wget http://127.0.0.1:8000/openapi.json -P docs/ --no-check-certificate

# Rename all "_id" in openapi.json to "id"
# This is done because the openapi spec generates the keys of the models with "_id" instead of "id"
# It is not a bug, it happens because the openapi spec uses alias of the keys used in the models
# For example, if a model has a field called "id", it will be renamed to "_id", because that's what mongodb uses
# But _is is considered a private member so "id" is used instead
sed -i 's/\"_id\"/\"id\"/g' docs/openapi.json

# Generate the python client
rm -rf sail-client/
openapi-python-client generate --path docs/openapi.json

# TODO: Generate a typescript client

# TODO: Generate a C# client

# Generate API documentation
redoc-cli bundle -o docs/index.html docs/openapi.json
