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
""" zojax.ui.portaltabs tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, event
from zope.app.testing import functional, setup
from zope.app.component.hooks import setSite
from zope.app.rotterdam import Rotterdam
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.interfaces import ISpace
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.ui.portaltabs.interfaces import IPortalTabsLayer


portalTabs = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'portalTabs', allow_teardown=True)


class IContent(IItem):
    """ content """


class Content(PersistentItem):
    interface.implements(IContent)


class IDefaultSkin(ILayoutFormLayer, Rotterdam, IPortalTabsLayer):
    """ skin """


def setUp(test):
    site = setup.placefulSetUp(True)


def tearDown(test):
    setup.placefulTearDown()


def FunctionalDocFileSuite(*paths, **kw):
    layer = portalTabs

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()
        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()

        # IIntIds
        root['intids'] = IntIds()
        sm.registerUtility(root['intids'], IIntIds)
        root['intids'].register(root)

        # default content
        content = Content(u'Content', u'Some Content')
        event.notify(ObjectCreatedEvent(content))
        IOwnership(content).ownerId = 'zope.user'
        root['content'] = content


    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        kw['optionflags'] = (doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    browser = FunctionalDocFileSuite(
        "tests.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    browser.layer = portalTabs

    configlet = doctest.DocFileSuite(
        "configlet.txt",
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    vocabulary = doctest.DocFileSuite(
        "vocabulary.txt",
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    return unittest.TestSuite((browser, configlet, vocabulary))
