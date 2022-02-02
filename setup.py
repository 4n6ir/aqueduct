from setuptools import setup

from aqueduct import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "aqueduct-utility",
    version = __version__,
    description = "Automate Cloud Development Kit (CDK) bootstrapping into an AWS Organization using Single Sign-On (SSO).",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/4n6ir/aqueduct",
    author = "John Lukach",
    author_email = "help@lukach.io",
    license = "Apache-2.0",
    packages = ["aqueduct"],
    install_requires = ["boto3","simple-term-menu"],
    zip_safe = False,
    entry_points = {
        "console_scripts": ["aqueduct=aqueduct.cli:main"],
    },
    python_requires = ">=3.7",
)
