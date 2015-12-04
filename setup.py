#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os
from setuptools import setup, find_packages


def parse_requirements():
    """Rudimentary parser for the `requirements.txt` file

    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = \
            map(str.strip, local_file('requirements.txt').splitlines())
    except IOError:
        raise RuntimeError("Couldn't find the `requirements.txt' file :(")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{0}=={1}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links

local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).read()

install_requires, dependency_links = parse_requirements()

if __name__ == '__main__':

    setup(
        name="markov",
        version='0.0.1',
        description="CLI wrapper for generating Markov chains from a text corpus",
        long_description=local_file('README.md'),
        author='Michael Walker',
        url='https://github.com/barrucadu/markov',
        packages=find_packages(exclude=['*tests*']),
        install_requires=install_requires,
        include_package_data=True,
        dependency_links=dependency_links,
        classifiers=[
            'Programming Language :: Python',
        ],
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'markov = markov.main:main'
            ],
        },
    )