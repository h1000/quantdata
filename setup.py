# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import quantdata
setup(
    name='quantdata',
    version=quantdata.__version__,
    description='A utility for crawling Quotes data of China stocks',
    author='jacob he',
    license='BSD',
    keywords='China stock data',
    classifiers=['Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: BSD License'],
    packages=['quantdata','quantdata.stock','quantdata.db','quantdata.script'],
    package_data={'': ['*.csv']},
)