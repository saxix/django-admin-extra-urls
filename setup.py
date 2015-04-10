#!/usr/bin/env python
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

dirname = 'admin_extra_urls'

app = __import__(dirname)


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
                 "django_dynamic_fixture",
                 "pytest-django",
                 "pytest-echo"]

install_requires = ["django>1.5,<1.8",
                    "six"],

setup(
    name=app.NAME,
    version=app.get_version(),
    description='Django mixin to easily add urls to any ModelAdmin',
    long_description=read("README.rst"),
    packages=find_packages('.'),
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
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: Developers'
    ]
)
