from setuptools import setup, find_packages

setup(
    name="wknml",
    packages=find_packages(exclude=("tests",)),
    version="0.0.3",
    install_requires=["loxun"],
    description="An NML library for webKnossos",
    author="Norman Rzepka",
    author_email="norman.rzepka@scalableminds.com",
    url="https://scalableminds.com",
)

