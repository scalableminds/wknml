# wknml
[![PyPI version](https://img.shields.io/pypi/v/wknml)](https://pypi.python.org/pypi/wknml)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/wknml.svg)](https://pypi.python.org/pypi/wknml)

Python library for working with [webKnossos](https://webknossos.org) [NML files](https://docs.webknossos.org/reference/data_formats#nml).

## Installation
To use wknml, you need to have Python 3.6+ (on the system or with Anaconda) installed.

```
pip install wknml
```

## Example Snippets
Some example to get you started. Make sure to also check the `examples` directory:
```python
# Load an NML file
with open("input.nml", "rb") as f:
    nml = wknml.parse_nml(f, nml)

# Access the most important properties
print(nml.parameters)
print(nml.trees)
print(nml.branchpoints)
print(nml.comments)
print(nml.groups)

# Iterate over all nodes
for tree in nml.trees:
    for node in tree.nodes:
        print(tree, node)

# Write a new NML file to disk
with open("out.nml", "wb") as f:
    wknml.write_nml(f, nml)

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
