import os
import re
import sys
from setuptools import setup, find_packages

packages = find_packages(exclude=['tests', 'tests.integration'])
requires = ['requests >= 2.0']

__version__ = ''
with open('betamax/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')

if sys.argv[-1] in ['submit', 'publish']:
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


def data_for(filename):
    with open(filename) as fd:
        content = fd.read()
    return content

setup(
    name="betamax",
    version=__version__,
    description="A VCR imitation for python-requests",
    long_description="\n\n".join([data_for("README.rst"),
                                  data_for("HISTORY.rst")]),
    license="Apache 2.0",
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github.com/sigmavirus24/betamax",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'pytest11': ['pytest-betamax = betamax.fixtures.pytest']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
