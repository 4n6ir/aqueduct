from setuptools import setup

from aqueduct import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "aqueduct-utility",
    version = __version__,
    description = "Cloud Development Kit Toolbox",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jblukach/aqueduct.git",
    author = "John Lukach",
    author_email = "hello@lukach.io",
    license = "Apache-2.0",
    packages = ["aqueduct"],
    install_requires = [
        "aws-sso-lib",
        "typer[all]"
    ],
    entry_points = {
        "console_scripts": [
            "aqueduct=aqueduct.aqueduct:app"
        ],
    },
    python_requires = ">=3.7",
)
