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
from zope import interface
from zope.component import getUtility

from interfaces import IPortalTab, IBoundPortalTab, IPortalTabsConfiglet


class PortalTab(object):

    id = None
    submenu = ()

    def __bind__(self, context, request):
        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        clone.context = context
        clone.request = request
        interface.directlyProvides(clone, IBoundPortalTab)
        return clone

    def getSubmenu(self):
        if self.submenu is None:
            return ()

        if not IBoundPortalTab.providedBy(self):
            return ()

        configlet = getUtility(IPortalTabsConfiglet)

        tabs = []
        for tabId in self.submenu:
            tab = configlet.getTab(tabId)
            if IPortalTab.providedBy(tab):
                tabs.append(tab.__bind__(self.context, self.request))

        return tabs
