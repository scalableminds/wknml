from setuptools import setup, find_packages

setup(
    name="wknml",
    packages=find_packages(exclude=("tests","examples")),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=["loxun"],
    description="An NML library for webKnossos",
    author="Norman Rzepka",
    author_email="norman.rzepka@scalableminds.com",
    url="https://scalableminds.com",
)

