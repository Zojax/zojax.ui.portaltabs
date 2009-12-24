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
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security.proxy import removeSecurityProxy

from zojax.ui.portaltabs.browser import portaltabs
from zojax.ui.portaltabs.interfaces import \
    IPortalTabsExtension, IPortalTabsConfiglet, IPortalTab


class PortalTabs2View(portaltabs.PortalTabsView):

    def tabs(self):
        tabs = getUtility(IPortalTabsConfiglet)
        id = getUtility(IIntIds).queryId(removeSecurityProxy(self.context))
        if id in tabs.registered:
            tab = tabs.getTab(id)
            if IPortalTab.providedBy(tab):
                tab = tab.__bind__(self.context, self.request)
                return tab.getSubmenu()
        return []
