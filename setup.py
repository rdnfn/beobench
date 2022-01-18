#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("PYPI_README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="UTF-8") as history_file:
    history = history_file.read()

version = "0.2.0"

requirements = [
    "wandb",
    "docker",
    "ray[rllib]",
    "click",
    "torch",
    "gym",
]


test_requirements = []

setup(
    author="rdnfn",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Beobench is a toolbox for benchmarking reinforcement learning (RL) algorithms on building energy optimisation (BEO) problems.",  # pylint: disable=line-too-long
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="beobench",
    name="beobench",
    packages=find_packages(include=["beobench", "beobench.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/rdnfn/beobench",
    zip_safe=False,
    version=version,
)
