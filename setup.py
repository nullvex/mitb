#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'py_pkg', '__version__.py')) as f:
#    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open("README.md", "r") as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name="mitb",
    description="Message In the Bottle manages a variety of enc/decrypt methods local and remote",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.9",
    author="nullvex",
    author_email="info@perpetual.media",
    url="__url__",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7.*",
    install_requires=["numpy", "requests"],
    license="__license__",
    zip_safe=False,
    entry_points={
        "console_scripts": ["mitb = mitb.__main__:mitb_init"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="package development template",
)
