#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='pycess',
      description='pycess',
      version='0.1',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Martin Häcker, Bernd Brincken',
      author_email='spamfaenger@gmx.de, brincken@orgraum.de',
      url='https://github.com/pycess/pycess',
      keywords='web wsgi django',
      
      packages=find_packages(),
      include_package_data=True,
#      zip_safe=False, Right now it should be
      test_suite='pycess',
      install_requires=[
          'django',
          'pyexpect'
      ],
)
