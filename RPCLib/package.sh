#!/bin/bash

tar -zcvf rpcrelated.tar.gz series.py test_server.py dataframe.py custom_typing.py private_keys public_keys zero
mv ./rpcrelated.tar.gz ../Docker/rpcrelated/
