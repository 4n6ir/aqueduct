from setuptools import setup

from aqueduct import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="aqueduct-utility",
    version=__version__,
    description="Automate Cloud Development Kit (CDK) bootstrapping into an AWS Organization using Single Sign-On (SSO) authentication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4n6ir/aqueduct",
    author="John Lukach",
    author_email="abuse@lukach.net",
    license="Apache-2.0",
    packages=["aqueduct"],
    zip_safe=False,
    entry_points={
        "console_scripts": ["aqueduct=aqueduct.cli:main"],
    },
    python_requires=">=3.6",
)
