#!/usr/bin/env python
import ast
import codecs
import os
import sys

import re
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'admin_extra_urls', '__init__.py')

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = os.getenv('PACKAGE_NAME',
                     str(ast.literal_eval(_name_re.search(content).group(1))))


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r").read()


tests_require =['coverage',
                'factory-boy',
                'django_webtest',
                'pdbpp',
                'pyquery',
                'pytest',
                'pytest-cov',
                'pytest-django',
                'pytest-echo',
                'pytest-pythonpath',
                'tox>=2.3',
                'wheel',
                ]
dev_require = ['autopep8',
               'check-manifest',
               'django',
               'flake8',
               'pep8',
               'readme',
               'sphinx',
               'wheel',
               'isort',
               ]

setup(
    name=name,
    version=version,
    url='https://github.com/saxix/django-admin-extra-urls',
    download_url='https://pypi.python.org/pypi/admin-extra-urls',

    description='Django mixin to easily add urls to any ModelAdmin',
    long_description=read("README.rst"),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    platforms=['linux'],
    extras_require={
        'test': tests_require,
        'dev': dev_require,
    },
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: Developers'
    ]
)
