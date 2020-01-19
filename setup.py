#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : Yehe
date   : 2020/1/18 16:28
role   : 
"""

from distutils.core import setup

__version__ = '0.0.1'

setup(
    name='yhops',
    version=__version__,
    packages=['yhops', 'yhops.devopssdk'],
    url='https://github.com/yehecarry/yhops.git',
    license='',
    install_requires=['pymysql==0.9.3', 'sqlalchemy==1.3.0', 'boto3'],
    author='Yehe',
    author_email='420636911@qq.com',
    description='yeops is operation  script'
)