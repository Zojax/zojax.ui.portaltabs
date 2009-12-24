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
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

from zojax.layoutform import button, Fields, PageletEditForm
from zojax.layoutform.interfaces import ICancelButton

from zojax.ui.portaltabs.interfaces import _
from zojax.ui.portaltabs.interfaces import IPortalTabsConfiglet
from zojax.ui.portaltabs.interfaces import IPortalTab, IObjectPortalTab

from configlet import PortalTabsBase


class ObjectPortalTab(PortalTabsBase, PageletEditForm):

    fields = Fields(IObjectPortalTab)
    label = _('Modify portal tab')

    buttons = PageletEditForm.buttons.copy()
    handlers = PageletEditForm.handlers.copy()

    @button.buttonAndHandler(_(u'Back'), name='back', provides=ICancelButton)
    def handleBack(self, action):
        self.redirect('../')

    @Lazy
    def configlet(self):
        return self.context.__parent__
