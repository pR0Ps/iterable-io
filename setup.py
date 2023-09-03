#!/usr/bin/env python

from setuptools import setup
import os.path


try:
    DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(DIR, "README.md"), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description=None


setup(
    name="iterable-io",
    version="1.0.0",
    description="Adapt generators and other iterables to a file-like interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pR0Ps/iterable-io",
    project_urls={
        "Source": "https://github.com/pR0Ps/iterable-io",
        "Changelog": "https://github.com/pR0Ps/iterable-io/blob/master/CHANGELOG.md",
    },
    license="LGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    py_modules=["iterableio"],
    python_requires=">=3.5",
)
