# database-initialization
This repository contains the scripts to initialize the database from the json file mentioned in the data folder.

## Getting started

Install for development for the first time:

```bash
make install
```
This will install the dependencies and the package in editable mode.
This will also install the sail-client dependency in the virtul environment.
The virtual environment is created in the .venv folder and can be activated using:
```bash
poetry shell
```

To exit the virtual environment:
```bash
deactivate
```

## Build the tool
```bash
poetry build
```
This will create a wheel file in the dist folder which can be installed using pip.

## Install the tool
```bash
pip install dist/database-initialization-0.1.0-py3-none-any.whl
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
