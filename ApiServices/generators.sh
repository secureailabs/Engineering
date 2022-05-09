# Download the API spec
wget http://127.0.0.1:8000/openapi.json -P docs/

# Generate API documentation
redoc-cli bundle -o docs/index.html docs/openapi.json
