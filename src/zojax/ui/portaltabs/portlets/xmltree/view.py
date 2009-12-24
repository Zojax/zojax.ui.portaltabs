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
from zope import interface, component
from zope.component import getUtility
from zope.publisher.interfaces import NotFound
from zope.security.proxy import removeSecurityProxy
from zope.location import LocationProxy, Location

from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet, IPortalTab


class PortalTabsView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.configlet = getUtility(IPortalTabsConfiglet)

    def publishTraverse(self, request, name):
        try:
            name = int(name)
        except (TypeError, ValueError):
            pass
        else:
            tab = self.configlet.getTab(name)
            if IPortalTab.providedBy(tab):
                tab = tab.__bind__(removeSecurityProxy(self.context), request)
                return LocationProxy(tab, self, name)

        raise NotFound(self, name, request)
