import sys

if sys.version_info >= (3, 7):
    from aqueduct.aqueduct import app
    app()
else:
    python_version = ".".join(map(str, sys.version_info[:3]))
    print("This utility requires Python >=3.7. Found {}".format(python_version))
    sys.exit(1)