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
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from zojax.richtext.field import RichTextProperty

from portaltab import PortalTab
from interfaces import IPortalTab, ISimplePortalTab, IPortalTabsConfiglet


class PortalTab(Persistent, PortalTab):
    interface.implements(ISimplePortalTab)

    submenu = ()
    
    description = RichTextProperty(ISimplePortalTab['description'])

    @property
    def configlet_title(self):
        return self.title
    
    def isSelected(self, strict=False):
        return False
