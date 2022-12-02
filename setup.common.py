"""Setup that only installs bugswarm.common and its dependencies. Used
to generate the bugswarm-common package on PyPI."""

from datetime import datetime

from setuptools import setup


today = datetime.utcnow()
version = f'{today.year}.{today.month:02}.{today.day:02}'

setup(
    name='bugswarm-common',
    version=version,
    url='https://github.com/BugSwarm/bugswarm',
    author='BugSwarm',
    author_email='dev.bugswarm@gmail.com',

    description='Library of modules used throughout the BugSwarm toolset',
    long_description='Library of modules used throughout the BugSwarm toolset',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    zip_safe=False,
    packages=['bugswarm.common'],
    install_requires=[
        'requests>=2.20.0',
        'CacheControl==0.12.3',
        'requests-cache==0.4.13',
    ],
)