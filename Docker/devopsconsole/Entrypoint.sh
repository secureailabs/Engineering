# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# Start each plugin
pushd plugins/SamplePlugin
python3 -m flask run --host=0.0.0.0 --port=5000 2>&1 | tee /app/SamplePlugin.log &
popd

# To prevent the docker container from exiting
tail -f /dev/null
