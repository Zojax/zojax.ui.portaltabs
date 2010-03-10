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
from zope.traversing.browser.absoluteurl import absoluteURL
"""

$Id$
"""
from zope import interface
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility, getMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.api import getPath
from zope.app.component.hooks import getSite

from zojax.resourcepackage.library import includeInplaceSource
from zojax.filefield.field import FileFieldProperty
from zojax.cache.view import cache
from zojax.portlet.cache import PortletModificationTag, PortletId
from zojax.ui.portaltabs.cache import PortalTabsTag
from zojax.portlet.browser.portlet import publicAbsoluteURL

from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet, IPortalTab, \
                                            IObjectPortalTab
                                            
from interfaces import IStaticMenuPortlet


def ViewAndContext(object, instance, *args, **kw):
    try:
        context = instance.manager.view.maincontext
    except AttributeError:
        context = instance.context
    return {'context': getPath(instance.context),
            'view': instance.view is not None and getPath(instance.view) or '',
            'principal': instance.request.principal.id,}


class MenuPortlet(object):
    
    headerImage = FileFieldProperty(IStaticMenuPortlet['headerImage'])

    def update(self):
        configlet = getUtility(IPortalTabsConfiglet)
        try:
            context = self.manager.view.maincontext
        except AttributeError:
            context = self.context
        tab = None
        if self.fromTab == 'context':
            tabs = []
            id = getUtility(IIntIds).queryId(removeSecurityProxy(context))
            if id in configlet.registered:
                tab = configlet.getTab(id)
                if IPortalTab.providedBy(tab):
                    tab = tab.__bind__(context, self.request)
        elif self.fromTab is not None:
            if self.fromTab in configlet.registered:
                tab = configlet.getTab(self.fromTab)
                if IPortalTab.providedBy(tab):
                    tab = tab.__bind__(context, self.request)
        if tab:
            fromTab = tab.id
            if IObjectPortalTab.providedBy(tab):
                self.context = tab.content
        else:
            fromTab = ''
        site_url = absoluteURL(getSite(), self.request)
        url = publicAbsoluteURL(self, self.request)
        self.id = url.replace(site_url, '').replace('/', '-').replace('.', '-')[1:]
        includeInplaceSource(menuinit%{'appUrl': site_url,
                                       'currUrl': self.request.URL[-1],
                                       'fromTab': fromTab,
                                       'hideSiblings': self.hideSiblings and 1 or 0,
                                       'id': self.id},
                             required=('zojax.ui.portaltabs',))

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

    @cache(PortletId(), ViewAndContext, PortletModificationTag, PortalTabsTag)
    def render(self):
        return super(MenuPortlet, self).render()


menuinit = """
<script type="text/javascript">
    $(document).ready( function() {
    new menu.MenuTree('%(id)s', '%(appUrl)s/', '%(currUrl)s/', '%(fromTab)s', %(hideSiblings)s);
  });
</script>
"""


class StaticMenuPortlet(object):
    
    headerImage = FileFieldProperty(IStaticMenuPortlet['headerImage'])

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
                       and list(result(tab.getSubmenu(), level+1)) or [],
                       'level': level
                       }
        self.tabs = list(result(tabs, 1))

    def isAvailable(self):
        return bool(self.tabs)

    @cache(PortletId(), ViewAndContext, PortletModificationTag, PortalTabsTag)
    def updateAndRender(self):
        return super(StaticMenuPortlet, self).updateAndRender()


class StaticMenuPortletView(object):

    template = ViewPageTemplateFile('staticportlet.pt')
