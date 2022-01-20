# Build the StructuredBufer shared library
make all -j

# Create a docker image
docker build -t python-structured-buffer .

# Run the docker image and mount the current directory
docker run -it --rm -v $(pwd):/app -p 5000:5000 python-structured-buffer

