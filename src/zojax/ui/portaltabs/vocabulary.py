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
from zope.component import getUtility, getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import IPortalTab, IPortalTabsConfiglet


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            try:
                return self.by_value[self.by_value.keys()[0]]
            except:
                pass


class TabsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        configlet = getUtility(IPortalTabsConfiglet)
        terms = []
        for id, tab in configlet.registered.items():
            if IPortalTab.providedBy(tab):
                terms.append((tab.configlet_title, id))
            else:
                terms.append(('Unknown', id))

        for name, tab in getUtilitiesFor(IPortalTab):
            terms.append((tab.configlet_title, name))

        terms.sort()
        return Vocabulary(
            [SimpleTerm(name,name,title) for title, name in terms])


class ToplevelTabsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        self.configlet = configlet = getUtility(IPortalTabsConfiglet)
        include = None
        filter_tab = False
        if IPortalTab.providedBy(context):
            include = context.submenu
            filter_tab = context.id

        if include is None:
            include = []

        seen = set()

        for id, tab in configlet.registered.items():
            if IPortalTab.providedBy(tab) and id not in seen:
                if tab.submenu is None:
                    continue
                if filter_tab in self.getSubmenu(tab):
                    seen.add(id)
                for id in tab.submenu:
                    seen.add(id)
        terms = []
        for id, tab in configlet.registered.items():
            if id not in seen or id in include:
                if id == filter_tab:
                    continue
                if IPortalTab.providedBy(tab):
                    terms.append((tab.configlet_title, id))
                else:
                    terms.append(('Unknown', id))

        terms.sort(key=lambda x: x[0])

        return Vocabulary(
            [SimpleTerm(name,name,title) for title, name in terms])

    def getSubmenu(self, tab):
        if not IPortalTab.providedBy(tab):
            raise StopIteration

        if tab.submenu is None:
            raise StopIteration

        for id in tab.submenu:
            yield id
            tab = self.configlet.getTab(id)
            for id in self.getSubmenu(tab):
                yield id
