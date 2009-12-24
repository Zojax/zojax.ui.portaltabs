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
"""

$Id$
"""
import random
from BTrees.OOBTree import OOBTree, OOTreeSet

from zope import interface, component
from zope.component import queryUtility, getUtilitiesFor
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin

from interfaces import IPortalTab, IPortalTabsConfiglet


class PortalTabsConfiglet(object):
    interface.implements(IPortalTabsConfiglet)

    def getTabs(self):
        data = self.data.get('tabs')
        if not data:
            return []
        return data

    def setTabs(self, value):
        self.data['tabs'] = value

    tabs = property(getTabs, setTabs)

    @property
    def registered(self):
        data = self.data.get('registered')
        if data is None:
            data = OOBTree()
            self.data['registered'] = data

        return data

    def getTab(self, tabId):
        tab = self.registered.get(tabId)
        if tab is None:
            tab = queryUtility(IPortalTab, tabId)

        return tab

    def getTabs(self, context, request):
        tabs = []
        seen = set()
        for tabId in self.tabs:
            if tabId in seen:
                continue
            seen.add(tabId)

            tab = self.getTab(tabId)
            if IPortalTab.providedBy(tab):
                tabs.append(tab.__bind__(context, request))

        return tabs

    def registerTab(self, tab):
        registered = self.registered

        if tab.id:
            id = tab.id
        else:
            id = random.randint(1, 10000)
            while id in registered:
                id += 1

            tab.id = id

        self.registered[id] = tab

        if id not in self.tabs:
            tabs = self.tabs
            tabs.append(id)
            self.tabs = tabs

    def unregisterTab(self, id):
        if id in self.registered:
            del self.registered[id]

            if id in self.tabs:
                tabs = self.tabs
                tabs.remove(id)
                self.tabs = tabs


class TraverserPlugin(object):
    interface.implements(ITraverserPlugin)
    component.adapts(IPortalTabsConfiglet, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        try:
            id = int(name)
        except:
            raise NotFound(self.context, name, request)

        tab = self.context.registered.get(id)
        if tab is None:
            raise NotFound(self.context, name, request)

        return LocationProxy(tab, self.context, name)
