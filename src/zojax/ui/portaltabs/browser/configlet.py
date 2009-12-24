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
from zope.traversing.browser import absoluteURL
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate import ViewPageTemplateFile
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.controlpanel.browser.configlet import Configlet

from zojax.ui.portaltabs.interfaces import _, IPortalTab


class PortalTabsBase(object):

    info = ViewPageTemplateFile('configlet.pt')

    def render(self):
        return super(PortalTabsBase, self).render() + self.info()

    def listRegistered(self):
        context = self.configlet
        request = self.request

        for tabId, tab in context.registered.items():
            if IPortalTab.providedBy(tab):
                yield tabId, tab.__bind__(context, request)
            else:
                yield tabId, tab

    @Lazy
    def configlet(self):
        return self.context

    def update(self):
        request = self.request

        if 'form.removeTab' in request:
            tabs = request.get('tabName', ())

            if not tabs:
                IStatusMessage(request).add(
                    _('Please select one of listed tabs.'), 'warning')
            else:
                for tabId in tabs:
                    self.configlet.unregisterTab(int(tabId))

                IStatusMessage(request).add(
                    _('Selected tabs have been removed.'))

        if 'form.addTab' in request:
            request.response.redirect(
                '%s/addportaltab.html' % absoluteURL(self.configlet, request))

        super(PortalTabsBase, self).update()


class PortalTabsConfiglet(PortalTabsBase, Configlet):
    pass
