#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Robert Alexander",
    author_email='raalexander.phi@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Computing a domain name by it's index",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='domain_name_label_indexes',
    name='domain_name_label_indexes',
    packages=find_packages(include=['domain_name_label_indexes', 'domain_name_label_indexes.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ralexander-phi/domain_name_label_indexes',
    version='0.1.1',
    zip_safe=False,
)
