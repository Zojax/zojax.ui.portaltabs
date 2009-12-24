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
from zope import interface, schema

from zojax.ui.portaltabs.interfaces import _


class IStaticMenuPortlet(interface.Interface):

    label = schema.TextLine(title=_(u'Label'),
                            required=False)

    level = schema.Int(title=_(u'Recursion level'),
                       description=_(u'0 - unrestricted'),
                       default=0)

    fromTab = schema.Choice(title = _(u'From Tab'),
                            vocabulary='portal.tabs.portlet',
                            required = False)
