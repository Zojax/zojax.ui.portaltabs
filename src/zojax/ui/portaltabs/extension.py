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
from persistent import Persistent
from rwproperty import getproperty, setproperty

from zope import interface, component
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.traversing.api import getParents
from zope.traversing.browser import absoluteURL
from zope.app.component.interfaces import ISite
from zope.app.folder.interfaces import IRootFolder

from portaltab import PortalTab
from interfaces import IObjectPortalTab
from interfaces import IPortalTabsConfiglet
from interfaces import IPortalTabsExtension


class PortalTabsExtension(object):
    interface.implements(IPortalTabsExtension)

    @getproperty
    def tabtitle(self):
        return self.data.get(
            'tabtitle', getattr(self.context, 'title', self.context.__name__))

    @setproperty
    def tabtitle(self, value):
        self.data['tabtitle'] = value

        if self.enabled:
            oid = getUtility(IIntIds).getId(self.context)

            configlet = getUtility(IPortalTabsConfiglet)
            configlet.registered[oid].title = value

    @getproperty
    def enabled(self):
        ids = getUtility(IIntIds)
        id = ids.queryId(self.context)

        if id is None:
            return False

        configlet = getUtility(IPortalTabsConfiglet)

        return id in configlet.registered

    @setproperty
    def enabled(self, value):
        oid = getUtility(IIntIds).queryId(self.context)
        if oid is None:
            return

        configlet = getUtility(IPortalTabsConfiglet)

        if value:
            configlet.registerTab(ObjectPortalTab(oid, self.tabtitle))
        else:
            configlet.unregisterTab(oid)

    @getproperty
    def visible(self):
        ids = getUtility(IIntIds)
        id = ids.queryId(self.context)

        if id is None:
            return False

        configlet = getUtility(IPortalTabsConfiglet)

        return id in configlet.tabs

    @setproperty
    def visible(self, value):
        oid = getUtility(IIntIds).queryId(self.context)
        if oid is None:
            return

        configlet = getUtility(IPortalTabsConfiglet)

        if value:
            if self.visible:
                return
            tabs = configlet.tabs
            tabs.append(oid)
            configlet.tabs = tabs
        else:
            if not self.visible:
                return
            tabs = configlet.tabs
            del tabs[configlet.tabs.index(oid)]
            configlet.tabs = tabs


class ObjectPortalTab(Persistent, PortalTab):
    interface.implements(IObjectPortalTab)

    submenu = None

    def __init__(self, oid, title):
        self.id = oid
        self.title = title

    @property
    def configlet_title(self):
        intids = getUtility(IIntIds)

        content = intids.queryObject(self.id)
        if content is None:
            return self.title

        configlet = getUtility(IPortalTabsConfiglet)

        res = []
        parent = content.__parent__
        if ISite.providedBy(content) or \
                parent is None or IRootFolder.providedBy(parent):
            return self.title

        try:
            title = configlet.registered[intids.getId(parent)].configlet_title
        except KeyError:
            title = getattr(parent, 'title', parent.__name__)

        return '/'.join([title, self.title])

    @property
    def url(self):
        try:
            return '%s/'%absoluteURL(self.content, self.request)
        except TypeError:
            return '#'

    def __bind__(self, context, request):
        clone = super(ObjectPortalTab, self).__bind__(context, request)
        clone.intids = getUtility(IIntIds)
        clone.content = clone.intids.queryObject(self.id)
        return clone

    def isSelected(self, strict=False):
        intids = self.intids
        context = self.context

        if ISite.providedBy(context):
            if self.id == intids.queryId(context):
                return True
            return False

        while context is not None and not ISite.providedBy(context):
            if self.id == intids.queryId(context):
                return True
            elif strict:
                return False

            context = getattr(context, '__parent__', None)

        return False
