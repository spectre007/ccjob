#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'string',
    'os',
    'subprocess',
    'glob',
    'json',
    're'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Alexander Zech",
    author_email='alexzech777@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Easy automation for quantum chemistry jobs.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='ccjob',
    name='ccjob',
    packages=find_packages(include=['ccjob', 'ccjob.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/spectre007/ccjob',
    version='0.1.0',
    zip_safe=False,
    )
