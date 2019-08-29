# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='Vesta',
    version='0.1.0',
    description='Asteroid game written using pygame',
    long_description=readme,
    author='Elliot Lunness',
    author_email='code@lazercube.com',
    url='https://github.com/LazerCube/vesta',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)