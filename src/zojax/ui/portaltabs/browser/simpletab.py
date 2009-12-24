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
from zope.location import LocationProxy
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.traversing.browser import absoluteURL

from zojax.layoutform.interfaces import ICancelButton
from zojax.layoutform import button, Fields, PageletAddForm, PageletEditForm

from zojax.ui.portaltabs.interfaces import _
from zojax.ui.portaltabs.simpletab import PortalTab
from zojax.ui.portaltabs.interfaces import ISimplePortalTab
from zojax.ui.portaltabs.interfaces import IObjectPortalTab, IPortalTab
from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet

from configlet import PortalTabsBase


class AddSimpleTabForm(PageletAddForm):

    label = _('Add Portal Tab')
    fields = Fields(ISimplePortalTab)

    def create(self, data):
        tab = PortalTab()
        for attr, value in data.items():
            setattr(tab, attr, value)

        return tab

    def add(self, tab):
        self.context.registerTab(tab)
        return tab

    def nextURL(self):
        tab = self._addedObject
        self._addedObject = LocationProxy(tab, self.context, str(tab.id))
        return u'%s/'%absoluteURL(self._addedObject, self.request)


class EditPortalTab(PortalTabsBase, PageletEditForm):

    fields = Fields(ISimplePortalTab)
    label = _('Modify portal tab')

    buttons = PageletEditForm.buttons.copy()
    handlers = PageletEditForm.handlers.copy()

    @button.buttonAndHandler(
        _(u'Back'), name='back', provides=ICancelButton)
    def handleBack(self, action):
        self.redirect('../')

    @Lazy
    def configlet(self):
        return self.context.__parent__
