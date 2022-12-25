This is a [cookiecutter](https://github.com/cookiecutter/cookiecutter)
template to generate the file structure for a Python project to be used in vscode

## Features

- [Poetry](https://python-poetry.org/) for dependency management
- Formatting with [black](https://pypi.org/project/black/) and [isort](https://pycqa.github.io/isort/index.html)
- Linting with [flake8](https://flake8.pycqa.org/en/latest/)
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)

## Quickstart

Install `cookiecutter` and directly pass the template location
or the template repository URL to the `cookiecutter` command.

``` bash
pip install cookiecutter
cookiecutter project-template
```

Install the environment and the pre-commit hooks with

 ```bash
 make install
 ```
