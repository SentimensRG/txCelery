#!/usr/bin/env python
from setuptools import setup

setup(
    name='txCelery',
    version='0.0.2 alpha',
    author='Sentimens Research Group, LLC',
    author_email='contact@sentimens.com',
    packages=['txcelery'],
    include_package_data=True,
    install_requires=['Twisted>=11.1.0', 'Celery>=3.1.16'],
    url='https://github.com/SentimensRG/txCelery',
    license='MIT',
    description=('Celery for Twisted:  manage Celery tasks from twisted'
                 'using the Deferred API'),
    keywords=["celery", "twisted", "deferred", "async", "asynchronous"],
    long_description=open('README.md').read()
)
