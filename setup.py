#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="astprint",
    version="1.0.0",
    description="AST printers",
    long_description=open("README.rst").read(),
    url="https://github.com/Manticore/astprint",
    author="Bogdan Opanchuk",
    author_email="bogdan@opanchuk.net",
    packages=find_packages(),
    install_requires=["six"],
    tests_require=["pytest"],
    platforms=["any"],
    keywords="AST printing",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
