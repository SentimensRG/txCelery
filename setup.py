#!/usr/bin/env python
from setuptools import setup


package_name = 'txcelery-py3'
package_version = '1.1.3'

setup(
    name='txcelery-py3',
    provides='txcelery',
    version=package_version,
    author='Sentimens Research Group, LLC',
    author_email='contact@sentimens.com',
    maintainer="Synerty Pty Ltd",
    maintainer_email="contact@synerty.com",
    packages=['txcelery'],
    include_package_data=True,
    install_requires=['Twisted>=11.0.0', 'Celery>=3.0.0', 'setuptools>=0.6'],
    url='https://github.com/Synerty/txcelery-py3',
    download_url=('https://github.com/Synerty/txcelery-py3/tarball/%s'
                  % package_version),
    license='MIT',
    description=('Celery for Twisted:  manage Celery tasks from twisted'
                 'using the Deferred API'),
    keywords=["celery", "twisted", "deferred", "async", "asynchronous"],
    long_description="""Celery for Twisted:
    Manage Celery tasks from twisted using the Deferred API""",
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ],
)
