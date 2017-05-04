#!/usr/bin/env python
import codecs
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

app = __import__('admin_extra_urls')


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

install_requires = ["six"]
setup_requires = []

if 'test' in sys.argv:
    setup_requires += tests_require


setup(
    name=app.NAME,
    version=app.get_version(),
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
        'tests': tests_require,
        'dev': dev_require + tests_require,
    },
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: Developers'
    ]
)
