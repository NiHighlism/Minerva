# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Minerva',
    version='1.0.0',
    description='Minerva - A RESTful API built with Flask',
    long_description=readme,
    author='Mukul Mehta',
    author_email='mukul.csiitkgp@gmail.com',
    url='https://github.com/mukul-mehta/minerva',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


