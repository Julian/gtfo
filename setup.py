import os

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="gtfo",
    url="https://github.com/Julian/gtfo",

    description="Flight search... please.",
    long_description=long_description,

    author="Julian Berman",
    author_email="Julian@GrayVines.com",

    packages=find_packages(),

    setup_requires=["vcversioner>=2.16.0.0"],
    vcversioner={"version_module_paths": ["gtfo/_version.py"]},

    install_requires=["attrs", "click", "hyperlink", "pyrsistent"],
    entry_points={"console_scripts" : ["gtfo = gtfo._cli:main"]},

    classifiers=classifiers,
)
