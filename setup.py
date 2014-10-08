#!/usr/bin/env python
import os
import codecs
from setuptools import setup, find_packages

dirname = 'admin_extra_urls'

app = __import__(dirname)


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r").read()


setup(
    name=app.NAME,
    version=app.get_version(),
    description='Django mixin to easily add urls to any ModelAdmin',
    long_description=read("README.rst"),
    packages=find_packages('.'),
    include_package_data=True,
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
