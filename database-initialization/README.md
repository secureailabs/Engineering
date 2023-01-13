# database-initialization
This repository contains the scripts to initialize the database from the json file mentioned in the data folder.

## Getting started

Install the environment and the pre-commit hooks with

```bash
make install
```

## Run the tool
```bash
database-initialization --hostname http://127.0.0.1:8000 --configuration configuration.json
```

## Call in a python script
```python
from database-initialization import initialize_database

initialize_database(
    hostname="http://127.0.0.1:8000",
    configuration="configuration.json",
)
```
sail-client = {path = "../ApiServices/generated/sail-client"}
