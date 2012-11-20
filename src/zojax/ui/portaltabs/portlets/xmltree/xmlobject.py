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
"""Support classes for XML-based tree

$Id$
"""
from rfc822 import formatdate, time
from xml.sax.saxutils import quoteattr

from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from zope.interface import Interface, implements
from zope.proxy import sameProxiedObjects
from zope.security.interfaces import Unauthorized, Forbidden
from zope.security.proxy import removeSecurityProxy
from zope.i18n import translate
from zope.traversing.api import getParents, getParent, traverse
from zope.traversing.browser import absoluteURL
from zope.publisher.browser import BrowserView

from zope.app.container.interfaces import IReadContainer
from zope.app.rotterdam.i18n import ZopeMessageFactory as _

from zojax.cache.view import cache
from zojax.cache.keys import PrincipalAndContext
from zojax.ui.portaltabs.cache import PortalTabsTag

from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet, IPortalTab
from interfaces import ISingleBranchTreeView

titleTemplate = _('Contains $${num} item(s)')
loadingMsg = _('Loading...')


def setNoCacheHeaders(response):
    """Ensure that the tree isn't cached"""
    response.setHeader('Pragma', 'no-cache')
    response.setHeader('Cache-Control', 'no-cache')
    response.setHeader('Expires',
                       formatdate(time.time() - 7 * 86400)) # 7 days ago


def xmlEscape(format, *args):
    quotedArgs = [quoteattr(unicode(arg)) for arg in args]
    return format % tuple(quotedArgs)


def xmlEscapeWithCData(format, *args):
    cData = args[-1]
    quotedArgs = [quoteattr(unicode(arg)) for arg in args[:-1]]
    quotedArgsWithCData = quotedArgs + [cData]
    return format % tuple(quotedArgsWithCData)


class XmlObjectView(BrowserView):
    """Provide a xml interface for dynamic navigation tree in UI"""

    implements(ISingleBranchTreeView)

    found_selected = False

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.configlet = getUtility(IPortalTabsConfiglet)

    def getIconUrl(self, item):
        result = ''
        icon = queryMultiAdapter((item, self.request), name='zmi_icon')
        if icon is not None:
            result = icon.url()
        return result

    def getLengthOf(self, item):
        return len(item.getSubmenu())

    def children_utility(self, container, deep=False):
        """Return an XML document that contains the children of an object."""
        result = []
        submenu=None
        try:
            submenu=container.getSubmenu()
        except AttributeError:
            pass
        if submenu:
            for item in submenu:

                iconUrl = self.getIconUrl(item)
                item_len = self.getLengthOf(item)
                selected = item.isSelected(True)
                if selected:
                    self.found_selected = True
                if not deep or self.found_selected:
                    result.append(xmlEscape(
                        u'<collection name=%s title=%s length=%s '
                        u'icon_url=%s url=%s selected=%s />',
                        item.id, item.title, item_len, iconUrl, item.url is not None and item.url or u'', selected and 1 or 0))
                else:
                    result.append(xmlEscapeWithCData(
                        u'<collection name=%s title=%s length=%s '
                        u'icon_url=%s url=%s selected=%s>%s</collection>',
                        item.id, item.title, item_len, iconUrl, item.url is not None and item.url or u'',
                        selected and 1 or 0,
                        self.children_utility(item, deep)))
            return u' '.join(result)
     


    def children(self):
        """ """
        container = self.context
        self.request.response.setHeader('Content-Type', 'text/xml')
        setNoCacheHeaders(self.request.response)
        res = (u'<?xml version="1.0" ?><children> %s </children>'
                % self.children_utility(container))
        return self.renderChildren(res)

    @cache('zojax.ui.portaltabs.children', PrincipalAndContext, PortalTabsTag)
    def renderChildren(self, res):
        return res

    def branch_utility(self):
        result = []
        fromTab = False
        if IPortalTab.providedBy(self.context):
            tabs = [self.context]
            fromTab = True
        else:
            tabs = self.configlet.getTabs(removeSecurityProxy(self.context), self.request)
        for item in tabs:
            subitem_len = self.getLengthOf(item)
            iconUrl = self.getIconUrl(item)
            if fromTab:
                selected = True
                have_selected = True
            else:
                selected = item.isSelected(True)
                have_selected = self.haveSelected(item)
            if selected:
                self.found_selected = True
            if have_selected:
                result.append(xmlEscapeWithCData(
                    u'<collection name=%s title=%s length=%s '
                    u'icon_url=%s url=%s selected=%s>%s</collection>',
                    item.id, item.title, subitem_len, iconUrl, item.url is not None and item.url or u'',
                    selected and 1 or 0, self.children_utility(item, True)))
            else:
                result.append(xmlEscape(
                    u'<collection name=%s title=%s length=%s '
                    u'icon_url=%s url=%s selected=%s />',
                    item.id, item.title, subitem_len, iconUrl, item.url is not None and item.url or u'',
                    selected and 1 or 0))

        cnt = len(result)
        return u' '.join(result), cnt

    def haveSelected(self, item):
        if item.isSelected(True):
            return True
        for item in item.getSubmenu():
            if self.haveSelected(item):
                return True
        return False

    def singleBranchTree(self, root=''):
        """Return an XML document with the siblings and parents of an object.

        There is only one branch expanded, in other words, the tree is
        filled with the object, its siblings and its parents with
        their respective siblings.

        """
        result, cnt = self.branch_utility()

        result = xmlEscapeWithCData(
                  u'<collection isroot="" length=%s>%s</collection>',
                  cnt,
                  result)

        self.request.response.setHeader('Content-Type', 'text/xml')
        setNoCacheHeaders(self.request.response)
        title = translate(titleTemplate,
                          context=self.request, default=titleTemplate)
        loading = translate(loadingMsg,
                          context=self.request, default=loadingMsg)
        return self.renderBranch(xmlEscapeWithCData(
                u'<?xml version="1.0" ?>'
                u'<children title_tpl=%s loading_msg=%s>%s</children>',
                title, loading, result))

    @cache('zojax.ui.portaltabs.branch', PrincipalAndContext, PortalTabsTag)
    def renderBranch(self, res):
        return res
