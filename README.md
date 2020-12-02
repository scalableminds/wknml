# wknml
[![PyPI version](https://img.shields.io/pypi/v/wknml)](https://pypi.python.org/pypi/wknml)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rasa.svg)](https://pypi.python.org/pypi/wknml)

Python library for working with [webKnossos](https://webknossos.org) [NML files](https://docs.webknossos.org/reference/data_formats#nml).

## Installation
To use wknml, you need to have Python 3.6+ (on the system or with Anaconda) installed.

```
pip install wknml
```

## Snippets
```
# Check out the repository and go into it
git clone git@github.com:scalableminds/wknml.git
cd wknml

# Convert an NML file with unlinked nodes to one with connected trees
python -m examples.fix_unlinked_nml <unlinked>.nml <fixed>.nml

```

# Development
Make sure to install all the required dependencies using Poetry:
```
pip install poetry
poetry install
```

Please, format and test your code changes before merging them.
```
poetry run black wknml tests examples
poetry run pytest tests
```

PyPi releases are automatically pushed when creating a new Git tag/Github release. Make sure to bump the package version number manually:
```
poetry version <patch, minor, major>
```

# License

MIT License
