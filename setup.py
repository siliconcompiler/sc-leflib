#!/usr/bin/env python3

import os
import shutil
from skbuild import setup
from setuptools_scm import get_version

with open("README.md", "r", encoding="utf-8") as readme:
    long_desc = readme.read()


def parse_reqs():
    '''Parse out each requirement category from requirements.txt'''
    install_reqs = []
    extras_reqs = {}
    current_section = None  # default to install

    with open('requirements.txt', 'r') as reqs_file:
        for line in reqs_file.readlines():
            line = line.rstrip('\n')
            if line.startswith('#:'):
                # strip off '#:' prefix to read extras name
                current_section = line[2:]
                if current_section not in extras_reqs:
                    extras_reqs[current_section] = []
            elif not line or line.startswith('#'):
                # skip blanks and comments
                continue
            elif current_section is None:
                install_reqs.append(line)
            else:
                extras_reqs[current_section].append(line)

    return install_reqs, extras_reqs


# Let us pass in generic arguments to CMake via an environment variable, since
# our automated build servers need to pass in a certain argument when building
# wheels on Windows.
cmake_args = []
if 'SC_CMAKEARGS' in os.environ:
    cmake_args.append(os.environ['SC_CMAKEARGS'])

# Remove the _skbuild/ directory before running install procedure. This helps
# fix very opaque bugs we've run into where the install fails due to some bad
# state being cached in this directory. This means we won't get caching of build
# results, but since the leflib is small and compiles quickly, and a user likely
# won't have to perform many installs anyways, this seems like a worthwhile
# tradeoff.
if os.path.isdir('_skbuild'):
    print("Note: removing existing _skbuild/ directory.")
    shutil.rmtree('_skbuild')

skbuild_args = {
    'cmake_install_dir': 'sc_leflib',
    'cmake_args': cmake_args
}


install_reqs, extras_req = parse_reqs()

setup(
    name="sc-leflib",
    description="LEF parser for SiliconCompiler",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    author="ZeroASIC",
    author_email="gadfort@zeroasic.com",
    url="https://siliconcompiler.com",
    project_urls={
        "Documentation": "https://docs.siliconcompiler.com",
        "Source Code": "https://github.com/siliconcompiler/sc-leflib",
        "Bug Tracker": "https://github.com/siliconcompiler/sc-leflib/issues",
        "Forum": "https://github.com/siliconcompiler/sc-leflib/discussions"
    },
    version=get_version(),
    packages=["sc_leflib"],

    python_requires=">=3.6",
    install_requires=install_reqs,
    extras_require=extras_req,
    **skbuild_args
)
