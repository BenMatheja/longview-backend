# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ''

setup(
    name='longview-backend',
    version='0.00.01',
    packages=['longview', 'longview.managers'],
    author='Ben Matheja',
    author_email='post@benmatheja.de',
    license='BSD',
    description='longview-backend - A Flask Restful Service to obtain performance metrics from the longview agent',
    long_description = read('README.md'),
    install_requires=[
        'requests',
        'flask',
        'gunicorn',
    ],
    # see here for complete list of classifiers
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ),
)
