##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zojax.ui.portaltabs package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0'


setup(name='zojax.ui.portaltabs',
      version=version,
      description="Portal tabs - extension for zojax site",
      long_description=(
        'Detailed Documentation\n' +
        '======================\n'
        + '\n\n' +
        read('CHANGES.txt')
        ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author='Nikolay Kim, Anatoly Bubenkov',
      author_email='fafhrd91@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax','zojax.ui'],
      install_requires = ['setuptools', 'rwproperty',
                          'ZODB3',
                          'zope.component',
                          'zope.interface',
                          'zope.schema',
                          'zope.publisher',
                          'zope.i18nmessageid',
                          'zope.traversing',
                          'zope.viewlet',
                          'zope.app.intid',
                          'zope.app.pagetemplate',
                          'z3c.traverser',
                          'zojax.cache',
                          'zojax.skintool',
                          'zojax.pageelement',
                          'zojax.layoutform',
                          'zojax.extensions',
                          'zojax.controlpanel',
                          'zojax.statusmessage',
                          'zojax.content.type',
                          'zojax.content.browser',
                          'zojax.content.forms',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zope.securitypolicy',
                                  'zojax.autoinclude',
                                  'zojax.content.space',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
