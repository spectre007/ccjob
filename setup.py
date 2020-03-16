#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# requirements = [
#     'string',
#     'os',
#     'subprocess',
#     'glob',
#     'json',
#     're'
# ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    # Self-descriptive entries
    name='ccjob',
    version='0.1.2',
    author="Alexander Zech",
    author_email='alexzech777@gmail.com',
    description="Easy automation for quantum chemistry jobs.",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    url='https://github.com/spectre007/ccjob',
    license="MIT license",
    keywords='ccjob',
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
    # Requirements
    python_requires='>=3.5',
    # install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    # test_suite='tests',

    # Which Python importable modules should be included when your package is installed
    # Handled automatically by setuptools. Use 'exclude' to prevent some specific
    # subpackage(s) from being added, if needed
    packages=find_packages(include=['ccjob', 'ccjob.*']),

    # Optional include package data to ship with your package
    # Customize MANIFEST.in if the general case does not suit your needs
    # Comment out this line to prevent the files from being packaged with your software
    include_package_data=True,

    # Manual control if final package is compressible or not,
    # set False to prevent the .egg from being made
    # zip_safe=False,
    )
