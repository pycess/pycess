#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(name='pycess',
      description='pycess',
      version='0.20',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      author='Martin Häcker, Bernd Brincken',
      author_email='spamfaenger@gmx.de, brincken@orgraum.de',
      url='https://github.com/pycess/pycess',
      keywords='web wsgi django',

      packages=find_packages(),
      include_package_data=True,
      #      zip_safe=False, Right now it should be
      test_suite='pycess.testing.runtests.runtests',
      install_requires=[
          'Django',
          'pyexpect',
          'splinter',
          'django-crispy-forms',
      ],
      )
