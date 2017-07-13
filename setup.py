#!/usr/bin/env python
from setuptools import setup

setup(
    name='txcelery-py3',
    version='1.2.0',
    author='Original author, Sentimens Research Group, LLC',
    author_email='contact@sentimens.com',
    packages=['txcelery'],
    include_package_data=True,
    install_requires=['Twisted>=11.0.0', 'Celery>=3.0.0', 'setuptools>=0.6'],
    url='https://github.com/Synerty/txcelery-py3',
    license='MIT',
    description=('Celery for Twisted:  manage Celery tasks from twisted'
                 'using the Deferred API'),
    keywords=["celery", "twisted", "deferred", "async", "asynchronous"],
    long_description=open('README.md').read()
)
