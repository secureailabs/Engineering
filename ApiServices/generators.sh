# delete existing openapi.json
rm -f docs/openapi.json

# Download the API spec
wget https://127.0.0.1:8000/openapi.json -P docs/ --no-check-certificate

# Generate API documentation
redoc-cli bundle -o docs/index.html docs/openapi.json
