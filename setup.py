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


class PyTest(TestCommand):

    def finalize_options(self):
        sys.path.append(os.path.join(os.path.dirname(__file__), "tests"))
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--ds', 'demo.settings']
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


tests_require = read('src/requirements/testing.pip')
dev_require = read('src/requirements/develop.pip')

install_requires = []
setup_requires = []

if 'test' in sys.argv:
    setup_requires += tests_require

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
    install_requires=install_requires,
    setup_requires=setup_requires,
    platforms=['linux'],
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require,
    },
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: Developers'
    ]
)
