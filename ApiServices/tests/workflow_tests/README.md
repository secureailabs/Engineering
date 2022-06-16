# Secure AI Labs

## PREREQUISITE

- Navigate to root of Project ApiServices
- Run ./build/test_setup.sh
- test_setup.sh: Will install Python 3.8 and add python to PATH
- test_setup.sh: Will create a virtual environment: `venv38-sail_test`
- test_setup.sh: Will install dependencies on your Virtual env (venv): `pip install -r requirements.txt`
- Activate your Virtual env (venv): `.\venv38-sail_test\Scripts\activate` OR `source venv38-sail_test/bin/activate`

- If running the test_orchestrator suite update config.py to have ORCHESTRATOR_PATH reflect the directory where your Orchestrator python libraries are

## Run active Tests
> `-m`
> : This is OPTIONAL param used to help specify groupings of tests, refer to pytest.ini for more info
> `--ip`
> : This is OPTIONAL param used to specify SAIL API portal ip. Defaults to value in Config.py

> `--port`
> : This is OPTIONAL param used to specify SAIL API portal port. Defaults to value in Config.py

> `--junitxml=result.xml`
> : This is OPTIONAL param used to capture test logs into result.xml

- Run Pytest: `pytest <ABS_dir>/test.py -m fastapi -sv --ip <ip> --port <port> --junitxml=result.xml`
- Example: `pytest workflow_tests/test_api/test_backend/sail_portal_api_test.py  -m fastapi -sv --ip 1.2.3.4 --port 6200 --junitxml=result.xml`

## Run Orchestrator Tests
- Specify local `ORCHESTRATOR_PATH` in global config.py
- Run Pytest for all active Orchestrator tests: `pytest workflow_tests/test_api/test_orchestrator/ -m active -sv --ip 1.2.3.4 --port 6200 --junitxml=result.xml`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`
