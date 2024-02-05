"""Packaging logic for betamax."""
import os
import re
import sys

import setuptools

packages = setuptools.find_packages(
    "src",
    exclude=["tests", "tests.integration"],
)
requires = ["requests >= 2.0"]

__version__ = ""
with open("src/betamax/__init__.py", "r") as fd:
    reg = re.compile(r"__version__ = [\'']([^\'']*)[\'']")
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError("Cannot find version information")

if sys.argv[-1] in ["submit", "publish"]:
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


def data_for(filename):
    """Read the file data for a filename."""
    with open(filename) as fd:
        content = fd.read()
    return content


setuptools.setup(
    name="betamax",
    version=__version__,
    description="A VCR imitation for python-requests",
    long_description="\n\n".join([data_for("README.rst"),
                                  data_for("HISTORY.rst")]),
    license="Apache 2.0",
    author="Ian Stapleton Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github.com/sigmavirus24/betamax",
    packages=packages,
    package_dir={"": "src"},
    package_data={"": ["LICENSE", "AUTHORS.rst"]},
    include_package_data=True,
    install_requires=requires,
    entry_points={
        "pytest11": ["pytest-betamax = betamax.fixtures.pytest"]
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)
