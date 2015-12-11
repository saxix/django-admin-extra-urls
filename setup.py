#!/usr/bin/env python
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(ROOT, 'src'))
import admin_extra_urls as app


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r").read()


setup_requires = []
if 'test' in sys.argv:
    setup_requires.append('pytest')


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


tests_require = ["tox>=1.8",
                 "django_webtest",
                 "pytest",
                 "wheel",
                 "django_dynamic_fixture",
                 "pytest-pythonpath",
                 "pytest-django",
                 "pytest-echo"]

install_requires = ["six"],

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
    platforms=['linux'],
    extras_require={
        'tests': tests_require,
    },
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: Developers'
    ]
)
