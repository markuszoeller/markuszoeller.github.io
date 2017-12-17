#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'docopt',
]

setup_requirements = [
]

test_requirements = [
    'flake8',
    'mock'
]

setup(
    name='tsk_mgr',
    version='0.1.0',
    description="Task Manager",
    long_description=readme + '\n\n' + history,
    author="Markus Zoeller",
    author_email='bogus@nope.com',
    url='https://github.com/markuszoeller/tsk_mgr',
    packages=find_packages(include=['tsk_mgr']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tsk_mgr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
