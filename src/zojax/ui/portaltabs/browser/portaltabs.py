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
from zope.security.proxy import removeSecurityProxy
from zojax.cache.view import cache
from zojax.cache.ids import PageElementId
from zojax.ui.portaltabs.cache import PortalTabsTag
from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet


def PortalTabsKey(object, instance, *args, **kw):

    def getTabs(tabs):
        for tab in tabs:
            yield tab
            for subtab in tab.getSubmenu():
                if subtab.isSelected():
                    yield subtab
                getTabs(subtab)
    tabs = tuple(getTabs(instance.tabs))
    selected = tuple((tab.id for tab in tabs if tab.isSelected()))
    return {'tabs': tuple((tab.id for tab in tabs)),
            'selected': selected}


class PortalTabsView(object):

    def __init__(self, context, request, view, manager=None):
        super(PortalTabsView, self).__init__(context, request, view, manager)

        self.tabs = getUtility(IPortalTabsConfiglet).getTabs(
            removeSecurityProxy(self.context), self.request)

    @cache(PageElementId(), PortalTabsTag, PortalTabsKey)
    def updateAndRender(self):
        return super(PortalTabsView, self).updateAndRender()
