#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("PYPI_README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="UTF-8") as history_file:
    history = history_file.read()

version = "0.5.3"  # pylint: disable=invalid-name

requirements = [
    "docker",
    "click",
    "pyyaml",
    "importlib-resources",  # backport of importlib.resources, required for Python<=3.8
    "loguru",
]

# The extended requirements are only used inside experiment/gym containers
extended_requirements = [
    "gym",
    "wandb",
]

rllib_requirements = [
    "ray[rllib]",
    "torch",
    "gym",
    "wandb",
]

setup(
    author="Beobench authors",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Beobench is a toolkit providing easy and unified access to building control environments for reinforcement learning (RL).",  # pylint: disable=line-too-long
    install_requires=requirements,
    extras_require={
        "extended": extended_requirements,
        "rllib": rllib_requirements,
    },
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="beobench",
    name="beobench",
    packages=find_packages(include=["beobench", "beobench.*"]),
    entry_points={
        "console_scripts": [
            "beobench = beobench.cli:cli",
        ],
    },
    test_suite="tests",
    project_urls={
        "Documentation": "https://beobench.readthedocs.io/",
        "Code": "https://github.com/rdnfn/beobench",
        "Issue tracker": "https://github.com/rdnfn/beobench/issues",
    },
    zip_safe=False,
    version=version,
)
