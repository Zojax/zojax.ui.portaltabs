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
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility, getMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.app.pagetemplate import ViewPageTemplateFile
from zojax.resourcepackage.library import include

from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet, IPortalTab


class MenuPortlet(object):

    def render(self):
        include('zojax.ui.portaltabs')
        return super(MenuPortlet, self).render()

    def isAvailable(self):
        try:
            context = self.manager.view.maincontext
        except AttributeError:
            try:
                context = self.view.context
            except AttributeError:
                context = self.context

        return bool(getMultiAdapter(
                (context, self.request),
                name='menuSingleBranchTree.xml').branch_utility()[1])


class StaticMenuPortlet(object):

    def update(self):
        configlet = getUtility(IPortalTabsConfiglet)
        try:
            context = self.manager.view.maincontext
        except AttributeError:
            context = self.context

        if self.fromTab == 'context':
            tabs = []
            id = getUtility(IIntIds).queryId(removeSecurityProxy(context))
            if id in configlet.registered:
                tab = configlet.getTab(id)
                if IPortalTab.providedBy(tab):
                    tab = tab.__bind__(context, self.request)
                    tabs = tab.getSubmenu()

        elif self.fromTab is not None:
            tabs = []
            if self.fromTab in configlet.registered:
                tab = configlet.getTab(self.fromTab)
                if IPortalTab.providedBy(tab):
                    tab = tab.__bind__(context, self.request)
                    tabs = [tab]
        else:
            tabs = configlet.getTabs(removeSecurityProxy(context), self.request)

        def result(tabs, level):
            for tab in tabs:
                yield {'tab': tab,
                       'submenu': (
                        (self.level and level<self.level) or not self.level)
                       and list(result(tab.getSubmenu(), level+1)) or []
                       }
        self.tabs = list(result(tabs, 1))

    def isAvailable(self):
        return bool(self.tabs)


class StaticMenuPortletView(object):

    template = ViewPageTemplateFile('staticportlet.pt')
