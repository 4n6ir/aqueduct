import sys

if sys.version_info >= (3, 6):
    from aqueduct.cli import main
    main()
else:
    python_version = ".".join(map(str, sys.version_info[:3]))
    print("This utility requires Python >=3.6. Found {}".format(python_version))
    sys.exit(1)