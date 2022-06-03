# Secure AI Labs

## Setup
- Install Python 3.8 and add python to PATH
- Clone SailTAP Repo
- Create a virtual environment: `python -m venv <name_venv>`
- Activate your Virtual env (venv): `.\<name_venv>\Scripts\activate` OR `source <name_venv>/bin/activate`
- Install dependencies on your Virtual env (venv): `pip install -r requirements.txt`
- If running the test_orchestrator suite update config.py to have ORCHESTRATOR_PATH reflect the directory where your Orchestrator python libraries are

## Run active Tests
> `--ip`
> : This is OPTIONAL param used to specify SAIL API portal ip. Defaults to value in Config.py

> `--port`
> : This is OPTIONAL param used to specify SAIL API portal port. Defaults to value in Config.py

> `--junitxml=result.xml`
> : This is OPTIONAL param used to capture test logs into result.xml

- Run Pytest: `pytest test_api/sail_api_test.py -m active -sv --ip <ip> --port <port> --junitxml=result.xml`
- Example: `pytest test_api/test_backend/account_mgmt_api_test.py -m active -sv --ip 1.2.3.4 --port 6200 --junitxml=result.xml`

## Run Orchestrator Tests
- Specify local `ORCHESTRATOR_PATH` in global config.py
- Run Pytest for all active Orchestrator tests: `pytest test_api/test_orchestrator/ -m active -sv --ip 1.2.3.4 --port 6200 --junitxml=result.xml`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`
