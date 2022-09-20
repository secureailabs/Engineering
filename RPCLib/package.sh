#!/bin/bash

tar -zcvf package.tar.gz series.py test_server.py dataframe.py custom_typing.py private_keys public_keys zero
mv ./package.tar.gz ../Docker/rpcrelated/
